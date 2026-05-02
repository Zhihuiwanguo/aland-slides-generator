from __future__ import annotations

import html
from datetime import date

import streamlit as st

THEMES = {
    "商务科技风": {
        "name": "business-tech",
        "bg": "#0B1020",
        "panel": "#131B33",
        "title": "#EAF2FF",
        "text": "#C7D6F5",
        "accent": "#35C2FF",
    },
    "艾兰得蓝色风": {
        "name": "aland-blue",
        "bg": "#0D2A6B",
        "panel": "#133A91",
        "title": "#F1F6FF",
        "text": "#D6E6FF",
        "accent": "#4EA1FF",
    },
    "浅绿色健康风": {
        "name": "health-green",
        "bg": "#EAF6EE",
        "panel": "#FFFFFF",
        "title": "#1F5130",
        "text": "#2F6A42",
        "accent": "#67B985",
    },
}


def build_slides_html(
    report_title: str,
    report_subtitle: str,
    audience: str,
    outline_lines: list[str],
    theme_key: str,
) -> str:
    theme = THEMES[theme_key]
    safe_title = html.escape(report_title.strip() or "未命名汇报")
    safe_subtitle = html.escape(report_subtitle.strip() or "")
    safe_audience = html.escape(audience.strip() or "通用")

    slides: list[str] = []
    cover = f"""
    <section class=\"slide cover\">
      <div class=\"content\">
        <h1>{safe_title}</h1>
        <h2>{safe_subtitle}</h2>
        <p class=\"meta\">目标受众：{safe_audience}</p>
        <p class=\"meta\">日期：{date.today().isoformat()}</p>
      </div>
    </section>
    """
    slides.append(cover)

    for i, line in enumerate(outline_lines, start=1):
        safe_line = html.escape(line)
        slides.append(
            f"""
            <section class=\"slide\">
              <div class=\"content\">
                <h2>第 {i} 页</h2>
                <p class=\"bullet\">{safe_line}</p>
              </div>
            </section>
            """
        )

    slides_html = "\n".join(slides)

    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{safe_title}</title>
  <style>
    :root {{
      --bg: {theme['bg']};
      --panel: {theme['panel']};
      --title: {theme['title']};
      --text: {theme['text']};
      --accent: {theme['accent']};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      display: grid;
      place-items: center;
      min-height: 100vh;
      overflow: hidden;
    }}
    .deck {{
      position: relative;
      width: min(96vw, 1600px);
      aspect-ratio: 16 / 9;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 20px 50px rgba(0,0,0,0.35);
      background: var(--panel);
    }}
    .slide {{
      position: absolute;
      inset: 0;
      padding: 8% 10%;
      opacity: 0;
      transform: translateX(30px);
      transition: opacity .35s ease, transform .35s ease;
      pointer-events: none;
      display: flex;
      align-items: center;
    }}
    .slide.active {{
      opacity: 1;
      transform: translateX(0);
      pointer-events: auto;
    }}
    h1 {{
      margin: 0 0 16px;
      color: var(--title);
      font-size: clamp(32px, 4vw, 64px);
      line-height: 1.2;
    }}
    h2 {{
      margin: 0 0 14px;
      color: var(--title);
      font-size: clamp(24px, 2.8vw, 44px);
    }}
    .bullet {{
      font-size: clamp(22px, 2.1vw, 34px);
      line-height: 1.5;
      border-left: 6px solid var(--accent);
      padding-left: 14px;
    }}
    .meta {{
      margin: 8px 0;
      font-size: clamp(16px, 1.3vw, 22px);
    }}
    .pager {{
      position: absolute;
      right: 24px;
      bottom: 16px;
      background: rgba(0,0,0,0.28);
      color: #fff;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <main class=\"deck\">
    {slides_html}
    <div class=\"pager\" id=\"pager\">1/{len(slides)}</div>
  </main>
  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    const pager = document.getElementById('pager');
    let index = 0;

    function render() {{
      slides.forEach((slide, i) => {{
        slide.classList.toggle('active', i === index);
      }});
      pager.textContent = `${{index + 1}}/${{slides.length}}`;
    }}

    function next() {{
      index = Math.min(index + 1, slides.length - 1);
      render();
    }}

    function prev() {{
      index = Math.max(index - 1, 0);
      render();
    }}

    document.addEventListener('keydown', (event) => {{
      if (event.key === 'ArrowRight') next();
      if (event.key === 'ArrowLeft') prev();
    }});

    document.addEventListener('click', (event) => {{
      const isLeft = event.clientX < window.innerWidth * 0.35;
      if (isLeft) prev(); else next();
    }});

    render();
  </script>
</body>
</html>
"""


st.set_page_config(page_title="艾兰得网页幻灯片生成器", layout="wide")
st.title("艾兰得网页幻灯片生成器")
st.caption("输入汇报信息，一键生成可下载的单文件 HTML 幻灯片。")

col1, col2 = st.columns(2)
with col1:
    report_title = st.text_input("汇报标题", value="2026Q2 经营汇报")
    report_subtitle = st.text_input("汇报副标题", value="渠道增长与效率优化")
with col2:
    audience = st.text_input("目标受众", value="管理层")
    style = st.selectbox("选择风格", options=list(THEMES.keys()))

outline = st.text_area(
    "幻灯片大纲（每行一页）",
    value="项目背景\n核心数据概览\n关键问题诊断\n解决方案与执行计划\n风险与下一步",
    height=180,
)

if st.button("生成幻灯片", type="primary"):
    lines = [line.strip() for line in outline.splitlines() if line.strip()]
    if not lines:
        st.error("请至少输入一行大纲内容。")
    else:
        html_content = build_slides_html(report_title, report_subtitle, audience, lines, style)
        st.success("幻灯片生成成功！")
        st.subheader("HTML 预览")
        st.components.v1.html(html_content, height=560, scrolling=False)
        st.download_button(
            label="下载 HTML 文件",
            data=html_content,
            file_name="aland_slides.html",
            mime="text/html",
        )
