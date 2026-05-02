from __future__ import annotations

import streamlit as st

from slides_generator import build_slides_html, parse_outline
from themes import THEMES

st.set_page_config(page_title="艾兰得网页幻灯片生成器 V0.3", layout="wide")
st.title("艾兰得网页幻灯片生成器 V0.3")
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
        st.download_button("下载 HTML 文件", data=html_content, file_name="aland_slides_v0_3.html", mime="text/html")
