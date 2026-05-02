from __future__ import annotations

import html
from datetime import date

from themes import THEMES

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
