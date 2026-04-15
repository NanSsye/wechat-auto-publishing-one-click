# Runbook

## 1. 安装 skill
复制整个 `wechat-auto-publishing-one-click/` 到 `~/.hermes/skills/`

## 2. 自举
```bash
bash scripts/bootstrap.sh
```

## 3. 工作目录
默认：`/home/nans/.hermes/wechat-ai-news/`

## 4. 单 cron
把 `templates/cron_prompt.txt` 作为 cron prompt。

## 5. 手动验证
看这些文件：
- `output/project_meta.json`
- `output/user_signals.json`
- `output/research_report.json`
- `output/asset_report.json`
- `output/architecture-diagram.html`
- `images/arch.png`
- `cover.png`
- `article.md`
- `output/preflight_report.json`
- `output/full_publish_result.json`
