from __future__ import annotations

import html
import re
from datetime import date

import streamlit as st

THEMES = {
    "商务科技风": {
        "bg": "linear-gradient(160deg, #0a1022 0%, #111c3f 60%, #16295a 100%)",
        "panel": "rgba(14, 24, 50, 0.72)",
        "title": "#ecf3ff",
        "text": "#c9d8f4",
        "accent": "#47c7ff",
        "pager_bg": "rgba(71, 199, 255, 0.18)",
        "pager_text": "#dff6ff",
    },
    "艾兰得蓝色风": {
        "bg": "linear-gradient(160deg, #08296e 0%, #0f429f 55%, #1e67d7 100%)",
        "panel": "rgba(8, 43, 112, 0.74)",
        "title": "#f1f7ff",
        "text": "#d7e7ff",
        "accent": "#68b0ff",
        "pager_bg": "rgba(140, 194, 255, 0.22)",
        "pager_text": "#f3f9ff",
    },
    "浅绿色健康营养风": {
        "bg": "linear-gradient(145deg, #e9f8ee 0%, #d6f0df 55%, #c4e8d1 100%)",
        "panel": "rgba(255, 255, 255, 0.78)",
        "title": "#1f5a37",
        "text": "#2f7048",
        "accent": "#66b68a",
        "pager_bg": "rgba(102, 182, 138, 0.18)",
        "pager_text": "#1f5a37",
    },
    "数据看板风": {
        "bg": "radial-gradient(circle at 20% 20%, #182846 0%, #0c1326 55%, #070b17 100%)",
        "panel": "rgba(11, 18, 34, 0.84)",
        "title": "#ecf4ff",
        "text": "#a8c1f0",
        "accent": "#00e6b8",
        "pager_bg": "rgba(0, 230, 184, 0.18)",
        "pager_text": "#d5fff5",
    },
    "黑金汇报风": {
        "bg": "linear-gradient(160deg, #0e0d0b 0%, #1b1710 60%, #2a2216 100%)",
        "panel": "rgba(22, 19, 14, 0.78)",
        "title": "#f7e6b0",
        "text": "#ddc793",
        "accent": "#d6a94f",
        "pager_bg": "rgba(214, 169, 79, 0.2)",
        "pager_text": "#f9eecf",
    },
    "小红书图文风": {
        "bg": "linear-gradient(160deg, #ffeef2 0%, #ffdce6 52%, #ffc9d9 100%)",
        "panel": "rgba(255, 255, 255, 0.86)",
        "title": "#d62958",
        "text": "#7d3750",
        "accent": "#ff4d7a",
        "pager_bg": "rgba(255, 77, 122, 0.17)",
        "pager_text": "#b5214a",
    },
}

TAG_PATTERN = re.compile(r"^\[(cover|agenda|content|kpi|summary)\]\s*(.*)$", re.IGNORECASE)


def parse_outline(raw: str) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m = TAG_PATTERN.match(line)
        if m:
            page_type = m.group(1).lower()
            page_body = m.group(2).strip()
        else:
            page_type = "content"
            page_body = line
        pages.append({"type": page_type, "body": page_body})
    return pages


def make_section(page: dict[str, str], idx: int) -> str:
    body = html.escape(page["body"])
    page_type = page["type"]
    if page_type == "cover":
        return f'<section class="slide cover"><div class="content"><h1>{body}</h1><p class="meta">{date.today().isoformat()}</p></div></section>'
    if page_type == "agenda":
        items = [f"<li>{html.escape(item.strip())}</li>" for item in page["body"].split("｜") if item.strip()]
        return f'<section class="slide agenda"><div class="content"><h2>目录</h2><ul class="agenda-list">{"".join(items)}</ul></div></section>'
    if page_type == "kpi":
        blocks = []
        for item in page["body"].split("｜"):
            if not item.strip():
                continue
            if ":" in item:
                k, v = item.split(":", 1)
            else:
                k, v = item, "-"
            blocks.append(f'<div class="kpi-card"><span class="kpi-key">{html.escape(k.strip())}</span><span class="kpi-value">{html.escape(v.strip())}</span></div>')
        return f'<section class="slide kpi"><div class="content"><h2>关键指标</h2><div class="kpi-grid">{"".join(blocks)}</div></div></section>'
    if page_type == "summary":
        return f'<section class="slide summary"><div class="content"><h2>总结</h2><p class="summary-text">{body}</p></div></section>'
    return f'<section class="slide content"><div class="content"><h2>内容页 {idx}</h2><p class="bullet">{body}</p></div></section>'


def build_slides_html(title: str, subtitle: str, audience: str, pages: list[dict[str, str]], theme_name: str) -> str:
    theme = THEMES[theme_name]
    safe_title = html.escape(title.strip() or "未命名汇报")
    safe_subtitle = html.escape(subtitle.strip() or "")
    safe_audience = html.escape(audience.strip() or "通用")

    sections = [
        f'<section class="slide intro"><div class="content"><h1>{safe_title}</h1><h2>{safe_subtitle}</h2><p class="meta">目标受众：{safe_audience}</p></div></section>'
    ]
    for idx, page in enumerate(pages, start=1):
        sections.append(make_section(page, idx))

    slides_html = "\n".join(sections)
    total = len(sections)

    return f"""<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{safe_title}</title>
<style>
:root{{--bg:{theme['bg']};--panel:{theme['panel']};--title:{theme['title']};--text:{theme['text']};--accent:{theme['accent']};--pager-bg:{theme['pager_bg']};--pager-text:{theme['pager_text']};}}
*{{box-sizing:border-box}}body{{margin:0;display:grid;place-items:center;min-height:100vh;background:var(--bg);font-family:"Segoe UI","PingFang SC",sans-serif;overflow:hidden}}
.deck{{position:relative;width:min(96vw,1600px);aspect-ratio:16/9;border-radius:18px;overflow:hidden;box-shadow:0 26px 60px rgba(0,0,0,.35)}}
.slide{{position:absolute;inset:0;padding:7% 9%;background:var(--panel);backdrop-filter: blur(4px);opacity:0;transform:translateX(28px) scale(.99);transition:all .4s ease;display:flex;align-items:center}}
.slide.active{{opacity:1;transform:translateX(0) scale(1);z-index:2}}
h1,h2{{color:var(--title);margin:0 0 14px}} h1{{font-size:clamp(32px,4vw,66px)}} h2{{font-size:clamp(24px,3vw,46px)}}
.meta,.bullet,.summary-text{{font-size:clamp(18px,1.6vw,30px);line-height:1.5;color:var(--text)}}
.bullet,.summary-text{{padding:14px 16px;border-left:6px solid var(--accent);background:rgba(255,255,255,.06);border-radius:8px}}
.agenda-list{{margin:10px 0 0;padding-left:24px;color:var(--text);font-size:clamp(20px,1.8vw,30px);line-height:1.8}}
.kpi-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;width:100%}}
.kpi-card{{border:1px solid rgba(255,255,255,.15);border-radius:14px;padding:18px;background:rgba(255,255,255,.06);display:flex;flex-direction:column;gap:8px}}
.kpi-key{{color:var(--text);font-size:clamp(16px,1.2vw,22px)}} .kpi-value{{color:var(--accent);font-size:clamp(26px,2.2vw,40px);font-weight:700}}
.pager{{position:absolute;right:20px;bottom:14px;background:var(--pager-bg);color:var(--pager-text);border:1px solid rgba(255,255,255,.2);padding:7px 13px;border-radius:999px;font-weight:600}}
</style></head><body><main class=\"deck\">{slides_html}<div id=\"pager\" class=\"pager\">1/{total}</div></main>
<script>
const slides=[...document.querySelectorAll('.slide')];const pager=document.getElementById('pager');let idx=0;
function render(){{slides.forEach((s,i)=>s.classList.toggle('active',i===idx));pager.textContent=`${{idx+1}}/${{slides.length}}`;}}
function next(){{idx=Math.min(idx+1,slides.length-1);render();}}function prev(){{idx=Math.max(idx-1,0);render();}}
document.addEventListener('keydown',(e)=>{{if(e.key==='ArrowRight')next();if(e.key==='ArrowLeft')prev();}});render();
</script></body></html>"""


st.set_page_config(page_title="艾兰得网页幻灯片生成器", layout="wide")
st.title("艾兰得网页幻灯片生成器")
st.caption("V0.2：支持页面类型标签与 6 套风格。")

left, right = st.columns(2)
with left:
    report_title = st.text_input("汇报标题", value="艾兰得拼多多经营分析系统")
    report_subtitle = st.text_input("汇报副标题", value="从经验运营到数据驱动")
with right:
    audience = st.text_input("目标受众", value="管理层 / 运营团队")
    style = st.selectbox("选择风格", list(THEMES.keys()))

outline = st.text_area(
    "幻灯片大纲（支持标签：cover / agenda / content / kpi / summary）",
    value="[cover] 艾兰得拼多多经营分析系统\n[agenda] 为什么做｜系统功能｜业务价值｜后续规划\n[content] 当前人工 Excel 分析效率低，口径不统一\n[kpi] GMV:100万｜ROI:1.9｜毛利率:35%\n[summary] 从经验运营走向数据化运营",
    height=220,
)

if st.button("生成幻灯片", type="primary"):
    parsed_pages = parse_outline(outline)
    if not parsed_pages:
        st.error("请至少输入一行内容。")
    else:
        output = build_slides_html(report_title, report_subtitle, audience, parsed_pages, style)
        st.success("V0.2 幻灯片已生成。")
        st.subheader("HTML 预览")
        st.components.v1.html(output, height=560, scrolling=False)
        st.download_button("下载 HTML 文件", data=output, file_name="aland_slides_v0_2.html", mime="text/html")
