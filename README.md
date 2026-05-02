# aland-slides-generator (V0.2)

一个基于 **Streamlit** 的网页幻灯片生成器：输入汇报信息和大纲，生成可直接打开的单文件 HTML 幻灯片。

## 功能

- Streamlit 网页界面
- 输入汇报标题 / 副标题 / 目标受众
- 输入幻灯片大纲（每行一页）
- 支持 page-type tags：
  - `[cover]`
  - `[agenda]`
  - `[content]`
  - `[kpi]`
  - `[summary]`
- 支持 6 套主题：
  - 商务科技风
  - 艾兰得蓝色风
  - 浅绿色健康营养风
  - 数据看板风
  - 黑金汇报风
  - 小红书图文风
- 生成单个 HTML 文件
- HTML 内联 CSS 和 JS
- 支持键盘左右键翻页
- Streamlit 页面支持 HTML 预览
- 支持下载 HTML 文件

## 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```

打开浏览器访问终端给出的本地地址（默认通常是 `http://localhost:8501`）。

## 大纲输入示例

```text
[cover] 2026Q2 经营汇报
[agenda] 增长回顾｜效率诊断｜行动计划
[content] 渠道增长的关键驱动因素
[kpi] GMV +18%，毛利率 +2.1pp，CAC -12%
[summary] 聚焦高价值渠道，推进自动化运营
```

> 若某一行未指定 tag，会按 `[content]` 处理。
