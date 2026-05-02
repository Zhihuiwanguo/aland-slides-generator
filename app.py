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
        "accent2": "#7AF2CE",
    },
    "艾兰得蓝色风": {
        "name": "aland-blue",
        "bg": "#0D2A6B",
        "panel": "#133A91",
        "title": "#F1F6FF",
        "text": "#D6E6FF",
        "accent": "#4EA1FF",
        "accent2": "#89C2FF",
    },
    "浅绿色健康营养风": {
        "name": "health-green",
        "bg": "#EAF6EE",
        "panel": "#FFFFFF",
        "title": "#1F5130",
        "text": "#2F6A42",
        "accent": "#67B985",
        "accent2": "#93D4AA",
    },
    "数据看板风": {
        "name": "dashboard",
        "bg": "#0A0F1A",
        "panel": "#111A2A",
        "title": "#E6F3FF",
        "text": "#B9D2EA",
        "accent": "#29D3FF",
        "accent2": "#7B7CFF",
    },
    "黑金汇报风": {
        "name": "black-gold",
        "bg": "#0C0C0C",
        "panel": "#1A1A1A",
        "title": "#F8E7B6",
        "text": "#E2D0A0",
        "accent": "#C8A44D",
        "accent2": "#F2D27A",
    },
    "小红书图文风": {
        "name": "xiaohongshu",
        "bg": "#FFF5F7",
        "panel": "#FFFFFF",
        "title": "#FF2850",
        "text": "#4D4D4D",
        "accent": "#FF5C7B",
        "accent2": "#FF9FB1",
    },
}

ALLOWED_TYPES = {"cover", "agenda", "content", "kpi", "summary"}


def parse_outline(outline_text: str) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    for raw in outline_text.splitlines():
        line = raw.strip()
        if not line:
            continue

        page_type = "content"
        content = line
        if line.startswith("[") and "]" in line:
            tag = line[1 : line.index("]")].strip().lower()
            if tag in ALLOWED_TYPES:
                page_type = tag
                content = line[line.index("]") + 1 :].strip()

        pages.append({"type": page_type, "content": content or "（待补充）"})

    return pages


def render_page_content(page: dict[str, str], idx: int, title: str, subtitle: str, audience: str) -> str:
    page_type = page["type"]
    content = html.escape(page["content"])

    if page_type == "cover":
        return f"""
        <section class=\"slide cover\">
          <div class=\"content\">
            <p class=\"tag\">COVER</p>
            <h1>{html.escape(title)}</h1>
            <h2>{html.escape(subtitle)}</h2>
            <p class=\"meta\">目标受众：{html.escape(audience)}</p>
            <p class=\"meta\">日期：{date.today().isoformat()}</p>
          </div>
        </section>
        """
    if page_type == "agenda":
        return f"""
        <section class=\"slide agenda\">
          <div class=\"content\">
            <p class=\"tag\">AGENDA</p>
            <h2>议程</h2>
            <p class=\"bullet\">{content}</p>
          </div>
        </section>
        """
    if page_type == "kpi":
        return f"""
        <section class=\"slide kpi\">
          <div class=\"content\">
            <p class=\"tag\">KPI</p>
            <h2>核心指标</h2>
            <div class=\"kpi-box\">{content}</div>
          </div>
        </section>
        """
    if page_type == "summary":
        return f"""
        <section class=\"slide summary\">
          <div class=\"content\">
            <p class=\"tag\">SUMMARY</p>
            <h2>总结与下一步</h2>
            <p class=\"bullet\">{content}</p>
          </div>
        </section>
        """

    return f"""
    <section class=\"slide content-page\">
      <div class=\"content\">
        <p class=\"tag\">CONTENT · {idx}</p>
        <h2>内容页</h2>
        <p class=\"bullet\">{content}</p>
      </div>
    </section>
    """


def build_slides_html(report_title: str, report_subtitle: str, audience: str, pages: list[dict[str, str]], theme_key: str) -> str:
    theme = THEMES[theme_key]
    safe_title = report_title.strip() or "未命名汇报"
    safe_subtitle = report_subtitle.strip() or ""
    safe_audience = audience.strip() or "通用"

    slides = [render_page_content(page, i + 1, safe_title, safe_subtitle, safe_audience) for i, page in enumerate(pages)]
    slides_html = "\n".join(slides)

    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{html.escape(safe_title)}</title>
  <style>
    :root {{
      --bg: {theme['bg']};
      --panel: {theme['panel']};
      --title: {theme['title']};
      --text: {theme['text']};
      --accent: {theme['accent']};
      --accent2: {theme['accent2']};
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; display: grid; place-items: center; min-height: 100vh; overflow: hidden; }}
    .deck {{ position: relative; width: min(96vw, 1600px); aspect-ratio: 16 / 9; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.35); background: radial-gradient(circle at 80% 0%, color-mix(in srgb, var(--accent2) 22%, transparent), transparent 40%), var(--panel); }}
    .slide {{ position: absolute; inset: 0; padding: 8% 10%; opacity: 0; transform: translateX(30px); transition: opacity .35s ease, transform .35s ease; pointer-events: none; display: flex; align-items: center; }}
    .slide.active {{ opacity: 1; transform: translateX(0); pointer-events: auto; }}
    .content {{ width: 100%; }}
    h1 {{ margin: 0 0 12px; color: var(--title); font-size: clamp(32px, 4vw, 64px); }}
    h2 {{ margin: 0 0 14px; color: var(--title); font-size: clamp(24px, 2.8vw, 44px); }}
    .tag {{ display: inline-block; margin: 0 0 14px; padding: 6px 10px; border-radius: 999px; font-size: 14px; background: color-mix(in srgb, var(--accent) 25%, transparent); border: 1px solid color-mix(in srgb, var(--accent) 60%, #ffffff); color: var(--title); }}
    .bullet {{ font-size: clamp(22px, 2.1vw, 34px); line-height: 1.5; border-left: 6px solid var(--accent); padding-left: 14px; }}
    .meta {{ margin: 8px 0; font-size: clamp(16px, 1.3vw, 22px); }}
    .kpi-box {{ margin-top: 12px; border: 2px dashed var(--accent); border-radius: 14px; padding: 18px 20px; font-size: clamp(24px, 2.4vw, 40px); color: var(--title); }}
    .pager {{ position: absolute; right: 24px; bottom: 16px; background: rgba(0,0,0,0.28); color: #fff; padding: 6px 12px; border-radius: 999px; font-size: 14px; }}
  </style>
</head>
<body>
  <main class=\"deck\">{slides_html}<div class=\"pager\" id=\"pager\">1/{len(slides)}</div></main>
  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    const pager = document.getElementById('pager');
    let index = 0;
    function render() {{ slides.forEach((s, i) => s.classList.toggle('active', i === index)); pager.textContent = `${{index + 1}}/${{slides.length}}`; }}
    function next() {{ index = Math.min(index + 1, slides.length - 1); render(); }}
    function prev() {{ index = Math.max(index - 1, 0); render(); }}
    document.addEventListener('keydown', (e) => {{ if (e.key === 'ArrowRight') next(); if (e.key === 'ArrowLeft') prev(); }});
    document.addEventListener('click', (e) => {{ e.clientX < window.innerWidth * 0.35 ? prev() : next(); }});
    render();
  </script>
</body>
</html>"""


st.set_page_config(page_title="艾兰得网页幻灯片生成器 V0.2", layout="wide")
st.title("艾兰得网页幻灯片生成器 V0.2")
st.caption("输入汇报信息，生成可预览、可下载的单文件 HTML 幻灯片。")

col1, col2 = st.columns(2)
with col1:
    report_title = st.text_input("汇报标题", value="2026Q2 经营汇报")
    report_subtitle = st.text_input("汇报副标题", value="渠道增长与效率优化")
with col2:
    audience = st.text_input("目标受众", value="管理层")
    style = st.selectbox("选择主题", options=list(THEMES.keys()))

outline = st.text_area(
    "幻灯片大纲（每行一页，可在行首使用 [cover]/[agenda]/[content]/[kpi]/[summary]）",
    value="[cover] 2026Q2 经营汇报\n[agenda] 增长回顾｜效率诊断｜行动计划\n[content] 渠道增长的关键驱动因素\n[kpi] GMV +18%，毛利率 +2.1pp，CAC -12%\n[summary] 聚焦高价值渠道，推进自动化运营",
    height=220,
)

if st.button("生成幻灯片", type="primary"):
    pages = parse_outline(outline)
    if not pages:
        st.error("请至少输入一行大纲内容。")
    else:
        html_content = build_slides_html(report_title, report_subtitle, audience, pages, style)
        st.success("幻灯片生成成功！")
        st.subheader("HTML 预览")
        st.components.v1.html(html_content, height=560, scrolling=False)
        st.download_button("下载 HTML 文件", data=html_content, file_name="aland_slides_v0_2.html", mime="text/html")
