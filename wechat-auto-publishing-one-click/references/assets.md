# Asset Rules

## Cover
- 必须是 GitHub 或 Twitter/X 的真实图片/截图
- 不得使用 AI 生成封面
- 不得使用纯文字底图
- 不得直接复用 `images/arch.png`

## Required body images
- `images/github_repo.png`
- `images/github_readme.png`
- `images/arch.png`

## asset_report.json schema
```json
{
  "project": "AIBrix",
  "generated_at": "ISO8601",
  "assets": [
    {
      "path": "cover.png",
      "source": "https://github.com/... or https://x.com/... or local real screenshot path",
      "purpose": "封面",
      "exists": true,
      "size_bytes": 12345,
      "format": "PNG",
      "dimensions": [900, 383]
    }
  ]
}
```

## Hard fail
如果 `cover.png` 的来源是：
- `local_generated_cover`
- `ai_generated`
- `text_card`

则 preflight 必须失败。