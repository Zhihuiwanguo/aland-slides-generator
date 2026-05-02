from __future__ import annotations

from io import BytesIO
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _pick_font():
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def _fig_to_bytes() -> bytes:
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=160)
    plt.close()
    buf.seek(0)
    return buf.read()


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def chart_product_sales_top10(product_df: pd.DataFrame) -> bytes | None:
    if product_df.empty:
        return None
    _pick_font()
    name_col = _find_col(product_df, ["标准产品名称", "产品名称", "商品名称"])
    value_col = _find_col(product_df, ["商家实收", "销售额", "GMV"])
    if not name_col or not value_col:
        return None
    df = product_df[[name_col, value_col]].dropna().head(10)
    if df.empty:
        return None
    plt.figure(figsize=(8.8, 4.8))
    plt.barh(df[name_col], df[value_col], color="#234B2C")
    plt.gca().invert_yaxis()
    plt.title("产品销售额 Top 10")
    return _fig_to_bytes()


def chart_product_profit_contrib(product_df: pd.DataFrame) -> bytes | None:
    if product_df.empty:
        return None
    _pick_font()
    name_col = _find_col(product_df, ["标准产品名称", "产品名称", "商品名称"])
    value_col = _find_col(product_df, ["扣推广后贡献毛利", "贡献毛利"])
    if not name_col or not value_col:
        return None
    df = product_df[[name_col, value_col]].dropna().head(10)
    if df.empty:
        return None
    colors = ["#00ACF8" if v >= 0 else "#B03A2E" for v in df[value_col]]
    plt.figure(figsize=(8.8, 4.8))
    plt.bar(df[name_col], df[value_col], color=colors)
    plt.xticks(rotation=30, ha="right")
    plt.title("产品扣推广后贡献毛利 Top/Bottom")
    return _fig_to_bytes()


def chart_baibu_compare(baibu_df: pd.DataFrame) -> bytes | None:
    if baibu_df.empty:
        return None
    _pick_font()
    cat_col = _find_col(baibu_df, ["类型", "分组", "标签", "场景"])
    if not cat_col:
        return None
    metric_cols = [c for c in ["商家实收", "推广费", "扣推广后贡献毛利"] if c in baibu_df.columns]
    if not metric_cols:
        return None
    df = baibu_df[[cat_col] + metric_cols].dropna(subset=[cat_col]).head(6)
    if df.empty:
        return None
    plot_df = df.set_index(cat_col)[metric_cols]
    plt.figure(figsize=(8.8, 4.8))
    plot_df.plot(kind="bar", ax=plt.gca(), color=["#234B2C", "#6E7F6A", "#00ACF8"])
    plt.title("百补 vs 日常 对比")
    plt.xticks(rotation=0)
    return _fig_to_bytes()


def chart_q2_progress(q2_kpi: dict[str, Any]) -> bytes | None:
    _pick_font()
    mapping = {
        "销售达成率": q2_kpi.get("销售达成率", 0),
        "ROI达成率": q2_kpi.get("ROI达成率", 0),
        "综合达成率": q2_kpi.get("综合达成率", 0),
    }
    vals = []
    for v in mapping.values():
        if isinstance(v, str):
            v = v.replace("%", "")
        try:
            vals.append(float(v))
        except Exception:
            vals.append(0.0)
    plt.figure(figsize=(8.6, 4.4))
    plt.bar(mapping.keys(), vals, color="#234B2C")
    plt.ylim(0, max(100, max(vals) * 1.25))
    plt.title("Q2 达成进度")
    return _fig_to_bytes()


def chart_link_roi_rank(link_df: pd.DataFrame) -> bytes | None:
    if link_df.empty:
        return None
    _pick_font()
    name_col = _find_col(link_df, ["链接标题", "商品ID", "链接名称"])
    roi_col = _find_col(link_df, ["实际ROI", "ROI"])
    if not name_col or not roi_col:
        return None
    df = link_df[[name_col, roi_col]].dropna().head(10)
    if df.empty:
        return None
    plt.figure(figsize=(8.8, 4.8))
    plt.barh(df[name_col], df[roi_col], color="#00ACF8")
    plt.gca().invert_yaxis()
    plt.title("链接 ROI 排名")
    return _fig_to_bytes()
