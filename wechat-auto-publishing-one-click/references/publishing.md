# Publishing

默认模式：`draft_only`

## Required env vars
- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`

## Publish command
优先：
```bash
node templates/publish.mjs
```

## Success rule
只要拿到有效 `media_id`，可视为草稿创建成功。

结果文件：
- `output/full_publish_result.json`

建议字段：
- success
- mode
- timestamp
- media_id
- thumb_media_id
- title
- summary
- author
- publish_status

## Reminder
API 自动正式发布不一定等于后台手动发布效果，所以默认只做草稿。作业成功的核心标准是：草稿创建成功 + 产物完整。 