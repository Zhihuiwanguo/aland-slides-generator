# aland-slides-generator (V0.2)

V0.2 聚焦“视觉升级”：6 套风格 + 5 种页面类型标签，继续保持单 HTML 导出与零复杂前端。

## V0.2 新增内容

- 新增 6 套风格：
  - 商务科技风
  - 艾兰得蓝色风
  - 浅绿色健康营养风
  - 数据看板风
  - 黑金汇报风
  - 小红书图文风
- 每套风格都包含独立：背景、标题、卡片、强调色、页码样式
- 新增页面类型标签：
  - `[cover]` 封面页
  - `[agenda]` 目录页
  - `[content]` 普通内容页
  - `[kpi]` 数据指标页
  - `[summary]` 总结页

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 输入示例

```text
[cover] 艾兰得拼多多经营分析系统
[agenda] 为什么做｜系统功能｜业务价值｜后续规划
[content] 当前人工 Excel 分析效率低，口径不统一
[kpi] GMV:100万｜ROI:1.9｜毛利率:35%
[summary] 从经验运营走向数据化运营
```

## Streamlit Cloud 部署

1. 推送到 GitHub（确保有 `app.py` + `requirements.txt`）
2. 打开 https://share.streamlit.io/
3. New app -> 选择仓库 -> Main file path 填 `app.py` -> Deploy
