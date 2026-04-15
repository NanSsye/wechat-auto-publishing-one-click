# wechat-auto-publishing-one-click

单技能打包版微信公众号自动发文方案。

特点：
- 单个 skill
- 单个 cron
- 内置真实封面规则
- 内置架构图 PNG 渲染
- 内置单 cron prompt 模板
- 内置 bootstrap 脚本
- 默认作者：老夏的金库

安装：
1. 复制 `wechat-auto-publishing-one-click/` 到 `~/.hermes/skills/`
2. 运行 `bash scripts/bootstrap.sh`
3. 参考 `templates/env.example.txt` 配置 `.env`
4. 把 `templates/cron_prompt.txt` 作为 cron prompt
