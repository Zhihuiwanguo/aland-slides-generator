from __future__ import annotations

import streamlit as st

from pptx_generator import build_pptx_from_report_pack
from report_pack_parser import load_report_pack, parse_report_pack
from slides_generator import build_slides_html, parse_outline
from themes import THEMES

st.set_page_config(page_title="艾兰得经营汇报 PPT 生成器", layout="wide")
st.title("艾兰得经营汇报 PPT 生成器")
st.caption("支持手动 HTML 预览，以及基于经营数据包生成正式 .pptx。")

mode = st.radio("生成模式", options=["经营数据包生成 PPTX", "手动 HTML 幻灯片"], index=0, horizontal=True)

if mode == "手动 HTML 幻灯片":
    col1, col2 = st.columns(2)
    with col1:
        report_title = st.text_input("汇报标题", value="2026Q2 经营汇报")
        report_subtitle = st.text_input("汇报副标题", value="渠道增长与效率优化")
    with col2:
        audience = st.text_input("目标受众", value="管理层")
        style = st.selectbox("选择主题", options=list(THEMES.keys()))

    outline = st.text_area("幻灯片大纲", height=220)
    if st.button("生成 HTML 幻灯片", type="primary"):
        pages = parse_outline(outline)
        if not pages:
            st.error("请至少输入一行大纲内容。")
        else:
            html_content = build_slides_html(report_title, report_subtitle, audience, pages, style)
            st.components.v1.html(html_content, height=560, scrolling=False)
            st.download_button("下载 HTML 文件", data=html_content, file_name="aland_slides.html", mime="text/html")
else:
    uploaded_file = st.file_uploader("上传经营系统导出的 JSON 数据包", type=["json"])
    if uploaded_file is not None:
        try:
            report_pack = load_report_pack(uploaded_file)
            parsed = parse_report_pack(report_pack)
            q2 = parsed["q2_kpi"]
            st.success("数据包解析成功")
            c1, c2, c3 = st.columns(3)
            c1.metric("当前销售额", q2.get("当前销售额", "N/A"))
            c2.metric("Q2销售目标", q2.get("Q2销售目标", "N/A"))
            c3.metric("销售达成率", q2.get("销售达成率", "N/A"))
            c4, c5, c6 = st.columns(3)
            c4.metric("当前实际ROI", q2.get("当前实际ROI", "N/A"))
            c5.metric("毛利率", q2.get("当前毛利率", "N/A"))
            c6.metric("奖金风险等级", q2.get("奖金风险等级", "N/A"))

            if st.button("生成经营汇报 PPTX", type="primary"):
                pptx_bytes = build_pptx_from_report_pack(report_pack)
                st.success("PPTX 生成成功")
                st.download_button(
                    "下载经营分析 PPTX",
                    data=pptx_bytes,
                    file_name="艾兰得拼多多经营分析报告.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
        except ValueError as exc:
            st.error(str(exc))
