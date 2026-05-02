from __future__ import annotations

import streamlit as st

from report_pack_parser import build_meta_from_report_pack, build_pages_from_report_pack, load_report_pack
from slides_generator import build_slides_html, parse_outline
from themes import THEMES

st.set_page_config(page_title="艾兰得网页幻灯片生成器 V0.3", layout="wide")
st.title("艾兰得网页幻灯片生成器 V0.3")
st.caption("输入汇报信息，生成可预览、可下载的单文件 HTML 幻灯片。")

mode = st.radio("生成模式", options=["手动大纲生成", "经营数据包生成"], index=0, horizontal=True)

if mode == "手动大纲生成":
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
else:
    st.subheader("上传经营分析数据包 JSON")
    uploaded_file = st.file_uploader("上传经营系统导出的 JSON 数据包", type=["json"])
    style = st.selectbox("选择主题", options=list(THEMES.keys()), key="pack_theme")

    if uploaded_file is not None:
        try:
            report_pack = load_report_pack(uploaded_file)
            meta = build_meta_from_report_pack(report_pack)
            pages = build_pages_from_report_pack(report_pack)
            q2_kpi = (((report_pack.get("summary") if isinstance(report_pack.get("summary"), dict) else {}).get("q2_kpi")) or {})

            st.success("数据包解析成功")
            st.write(f"**报告标题：** {meta['report_title']}")
            st.write(f"**页面数量：** {len(pages)}")
            st.write(f"**识别到的 Q2销售达成率：** {q2_kpi.get('销售达成率', '未识别')}")
            st.write(f"**识别到的 当前实际ROI：** {q2_kpi.get('当前实际ROI', '未识别')}")
            st.write(f"**识别到的 奖金风险等级：** {q2_kpi.get('奖金风险等级', '未识别')}")

            if st.button("生成经营汇报幻灯片", type="primary"):
                html_content = build_slides_html(meta["report_title"], meta["report_subtitle"], meta["audience"], pages, style)
                st.success("经营汇报幻灯片生成成功！")
                st.subheader("HTML 预览")
                st.components.v1.html(html_content, height=560, scrolling=False)
                st.download_button(
                    "下载 HTML 文件",
                    data=html_content,
                    file_name="aland_pdd_report_from_json.html",
                    mime="text/html",
                )
        except ValueError as exc:
            st.error(str(exc))
