---
name: wechat-auto-publishing-one-click
description: 单技能打包版微信公众号自动发文方案——内置选题调研、真实项目图片抓取、独立真实封面、架构图 PNG 生成、文章写作、preflight 校验、草稿发布、单 cron 提示词模板与自举脚本。目标是下载这一个 skill 后即可启用，不再额外依赖 architecture-diagram / orchestrator 等其他 skill。
version: 1.0.0
author: 老夏
tags: [wechat, official-account, publishing, cron, github, twitter, architecture-diagram, one-click]
---

# WeChat Auto Publishing One-Click

这是公众号自动发文的一体化 skill。

目标：
- 只装这一个 skill
- 一次性拿到完整工作流
- 单个 cron 内完成全流程
- 不再依赖额外 skill 才能工作

## 内置能力

1. 选题研究
2. 子 agent 并行调研模板
3. GitHub / Twitter 真实图片抓取规则
4. 独立真实封面规则
5. 架构图 HTML -> PNG 渲染
6. 文章模板与排版规则
7. preflight 校验
8. draft_only 发布
9. 单 cron 提示词模板
10. 自举安装脚本

## 强约束

- 封面禁止 AI 生图
- 封面必须来自 GitHub 或 Twitter/X 真实项目图片/截图
- 架构图主产物必须是 PNG
- 必须单 cron 内完成，不拆多个 cron
- 作者名默认固定：`老夏的金库`
- 默认发布模式：`draft_only`

## 你应该优先读这些文件

- `runbook.md`
- `references/workflow.md`
- `references/assets.md`
- `references/publishing.md`
- `templates/cron_prompt.txt`
- `templates/article-template.md`
- `scripts/bootstrap.sh`
- `scripts/render_arch_png.py`
- `scripts/make_real_cover.py`
- `assets/architecture_template.html`

## 使用方式

### 1. 自举环境

先运行：

```bash
bash scripts/bootstrap.sh
```

### 2. 准备工作目录

默认工作目录：

```text
/home/nans/.hermes/wechat-ai-news/
```

### 3. 单 cron 提示词

把 `templates/cron_prompt.txt` 的内容直接作为 Hermes cron prompt 使用。

### 4. 架构图生成

优先调用内置脚本：

```bash
python3 scripts/render_arch_png.py \
  --meta output/project_meta.json \
  --notes output/architecture_notes.md \
  --html output/architecture-diagram.html \
  --png images/arch.png
```

### 5. 封面生成

封面只能来自真实项目图：

```bash
python3 scripts/make_real_cover.py \
  --input images/github_repo.png \
  --fallback images/github_readme.png \
  --output cover.png
```

## 交付标准

至少生成：
- `output/project_candidates.json`
- `output/project_meta.json`
- `output/user_signals.json`
- `output/architecture_notes.md`
- `output/research_report.json`
- `output/asset_report.json`
- `output/architecture-diagram.html`
- `images/arch.png`
- `cover.png`
- `article.md`
- `output/preflight_report.json`
- `output/full_publish_result.json`

## 不完整即失败

以下任一缺失都不算成功：
- 没有真实封面
- 没有 GitHub/README 正文图
- 没有架构图 PNG
- 没有 preflight
- 没有 draft 发布结果

## 共享发布建议

如果要分享给别人：
- 直接分享整个 skill 目录
- 或发布本 skill 对应的 GitHub 仓库
- 让别人只需复制 skill + 运行 bootstrap + 配 `.env`

## 秘密边界

不要把真实 token、cookie、appid、secret 写进 skill。
只提供：
- 变量名
- 示例模板
- 脚本
- 工作流
