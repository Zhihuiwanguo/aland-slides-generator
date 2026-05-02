from __future__ import annotations

import json
from typing import Any


def load_report_pack(uploaded_file) -> dict[str, Any]:
    try:
        payload = uploaded_file.read()
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        report_pack = json.loads(payload)
    except Exception as exc:
        raise ValueError("JSON 文件无法解析，请确认是从经营系统导出的数据包") from exc

    if not isinstance(report_pack, dict):
        raise ValueError("数据包格式不正确")

    return report_pack


def _to_number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        raw = value.replace(",", "").replace("%", "").replace("¥", "").strip()
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            return None
    return None


def _format_metric(label: str, value: Any) -> str:
    if value is None or value == "":
        return ""

    number = _to_number(value)
    if number is None:
        return f"{label}：{value}"

    if any(key in label for key in ["ROI"]):
        return f"{label}：{number:.2f}"
    if any(key in label for key in ["率", "占比"]):
        return f"{label}：{number:.2f}%"
    if any(key in label for key in ["收", "销售", "毛利", "费", "金额", "安全线", "差", "目标"]):
        return f"{label}：¥{number:,.2f}"
    return f"{label}：{number:,.0f}"


def _pick_table_rows(report_pack: dict[str, Any], keyword: str) -> list[dict[str, Any]]:
    slides = report_pack.get("slides")
    if not isinstance(slides, list):
        return []

    for slide in slides:
        if not isinstance(slide, dict):
            continue
        title = str(slide.get("title", ""))
        if keyword in title:
            table = slide.get("table")
            if isinstance(table, list):
                return [r for r in table if isinstance(r, dict)]
    return []


def _rows_to_summary(rows: list[dict[str, Any]], limit: int = 5) -> str:
    lines: list[str] = []
    for row in rows[:limit]:
        name = row.get("产品名称") or row.get("链接名称") or row.get("名称") or row.get("商品") or "未命名"
        sales = row.get("销售额") or row.get("商家实收") or row.get("GMV")
        margin = row.get("毛利")
        roi = row.get("ROI")

        parts = [f"{name}"]
        if sales is not None:
            parts.append(_format_metric("销售", sales).replace("销售：", "销售 "))
        if margin is not None:
            parts.append(_format_metric("毛利", margin).replace("毛利：", "毛利 "))
        if roi is not None:
            parts.append(_format_metric("ROI", roi).replace("ROI：", "ROI "))
        lines.append("｜".join(parts))

    return "\n".join(lines) if lines else "暂无可展示数据"


def build_meta_from_report_pack(report_pack: dict[str, Any]) -> dict[str, str]:
    report_meta = report_pack.get("report_meta") if isinstance(report_pack.get("report_meta"), dict) else {}
    return {
        "report_title": report_meta.get("report_title") or "艾兰得拼多多经营分析报告",
        "report_subtitle": "经营总览 / Q2考核 / 推广效率 / 异常清单",
        "audience": "管理层",
    }


def build_pages_from_report_pack(report_pack: dict[str, Any]) -> list[dict[str, str]]:
    summary = report_pack.get("summary") if isinstance(report_pack.get("summary"), dict) else {}
    overview_metrics = summary.get("overview_metrics") if isinstance(summary.get("overview_metrics"), dict) else {}
    q2_kpi = summary.get("q2_kpi") if isinstance(summary.get("q2_kpi"), dict) else {}

    pages: list[dict[str, str]] = [
        {"type": "cover", "content": "艾兰得拼多多经营分析报告"},
        {
            "type": "agenda",
            "content": "经营总览｜Q2考核达成率｜达标缺口测算｜产品表现｜链接表现｜百补 vs 日常｜推广分析｜经营异常｜下阶段建议",
        },
    ]

    overview_labels = ["商家实收", "用户实付", "订单侧估算毛利", "店铺整体实际ROI", "店铺总盘推广费（现金口径）", "有效订单数"]
    overview_lines = [_format_metric(label, overview_metrics.get(label)) for label in overview_labels]
    overview_text = "\n".join([line for line in overview_lines if line]) or "暂无经营总览指标"
    pages.append({"type": "kpi", "content": f"经营总览\n{overview_text}"})

    q2_labels = ["当前销售额", "Q2销售目标", "销售达成率", "当前实际ROI", "Q2 ROI目标", "ROI达成率", "综合达成率", "当前毛利率", "奖金风险等级"]
    q2_lines = [_format_metric(label, q2_kpi.get(label)) for label in q2_labels]
    q2_text = "\n".join([line for line in q2_lines if line]) or "暂无Q2考核指标"
    pages.append({"type": "kpi", "content": f"Q2考核达成率\n{q2_text}"})

    gap_labels = ["70%销售安全线", "距离70%安全线还差", "距离100%销售目标还差", "达到70%安全线每日需完成销售额", "达到100%目标每日需完成销售额", "距离目标ROI还差"]
    gap_lines = [_format_metric(label, q2_kpi.get(label)) for label in gap_labels]
    gap_text = "\n".join([line for line in gap_lines if line]) or "暂无达标缺口测算数据"
    pages.append({"type": "content", "content": f"达标缺口测算\n{gap_text}"})

    pages.append({"type": "content", "content": f"产品表现 Top\n{_rows_to_summary(_pick_table_rows(report_pack, '产品表现'), 5)}"})
    pages.append({"type": "content", "content": f"链接表现 Top\n{_rows_to_summary(_pick_table_rows(report_pack, '链接表现'), 5)}"})
    pages.append({"type": "content", "content": f"百补 vs 日常\n{_rows_to_summary(_pick_table_rows(report_pack, '百补'), 5)}"})
    pages.append({"type": "content", "content": f"经营异常清单\n{_rows_to_summary(_pick_table_rows(report_pack, '异常'), 6)}"})

    suggestion = q2_kpi.get("经营建议") or "聚焦销售达成率、控制低效推广费、优化百补链接、放大利润规格。"
    pages.append({"type": "summary", "content": f"下阶段经营建议\n{suggestion}"})

    return pages
