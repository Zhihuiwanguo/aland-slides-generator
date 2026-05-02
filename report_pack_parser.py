from __future__ import annotations

import json
from typing import Any

import pandas as pd


def load_report_pack(uploaded_file) -> dict[str, Any]:
    try:
        payload = uploaded_file.read()
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        data = json.loads(payload)
    except Exception as exc:
        raise ValueError("JSON 文件无法解析，请确认是从经营系统导出的数据包") from exc

    if not isinstance(data, dict):
        raise ValueError("数据包格式不正确")
    return data


def _as_number(value: Any) -> float | int | None:
    if isinstance(value, (int, float)):
        return value
    if not isinstance(value, str):
        return None
    txt = value.replace(",", "").replace("%", "").replace("¥", "").strip()
    if not txt:
        return None
    try:
        num = float(txt)
        return int(num) if num.is_integer() else num
    except ValueError:
        return None


def _to_df(rows: Any) -> pd.DataFrame:
    if isinstance(rows, list):
        valid_rows = [r for r in rows if isinstance(r, dict)]
        if valid_rows:
            return pd.DataFrame(valid_rows)
    return pd.DataFrame()


def _find_table(report_pack: dict[str, Any], keyword: str) -> pd.DataFrame:
    for slide in report_pack.get("slides", []):
        if not isinstance(slide, dict):
            continue
        if keyword in str(slide.get("title", "")):
            return _to_df(slide.get("table"))
    return pd.DataFrame()


def _normalize_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    for col in out.columns:
        converted = out[col].map(_as_number)
        if converted.notna().any():
            out[col] = converted.where(converted.notna(), out[col])
    return out


def parse_report_pack(report_pack: dict[str, Any]) -> dict[str, Any]:
    summary = report_pack.get("summary") if isinstance(report_pack.get("summary"), dict) else {}
    report_meta = report_pack.get("report_meta") if isinstance(report_pack.get("report_meta"), dict) else {}
    overview_metrics = summary.get("overview_metrics") if isinstance(summary.get("overview_metrics"), dict) else {}
    q2_kpi = summary.get("q2_kpi") if isinstance(summary.get("q2_kpi"), dict) else {}

    cleaned_overview = {k: (_as_number(v) if _as_number(v) is not None else v) for k, v in overview_metrics.items()}
    cleaned_q2 = {k: (_as_number(v) if _as_number(v) is not None else v) for k, v in q2_kpi.items()}

    product_table = _normalize_numeric_columns(_find_table(report_pack, "产品表现"))
    link_table = _normalize_numeric_columns(_find_table(report_pack, "链接表现"))
    baibu_table = _normalize_numeric_columns(_find_table(report_pack, "百补"))
    abnormal_table = _normalize_numeric_columns(_find_table(report_pack, "异常"))

    advice_text = str(cleaned_q2.get("经营建议") or "")

    return {
        "report_meta": report_meta,
        "overview_metrics": cleaned_overview,
        "q2_kpi": cleaned_q2,
        "product_table": product_table,
        "link_table": link_table,
        "baibu_table": baibu_table,
        "abnormal_table": abnormal_table,
        "advice_text": advice_text,
    }
