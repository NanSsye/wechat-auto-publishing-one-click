# Workflow

单次运行的推荐阶段：

1. init
2. research
3. assets
4. architecture diagram
5. article
6. preflight
7. publish

## Stage 1: research
并行子任务：
- researcher：筛 GitHub 候选并落盘 `output/project_candidates.json`
- twitter_scout：收集公开用户反馈并落盘 `output/user_signals.json`
- architecture analyst：提炼架构与模块，落盘 `output/project_meta.json` + `output/architecture_notes.md`

汇总后生成：
- `output/research_report.json`

## Stage 2: assets
必须准备：
- `cover.png` —— 必须来自 GitHub 或 Twitter/X 真实图片/截图
- `images/github_repo.png`
- `images/github_readme.png`

禁止：
- AI 生图当封面
- 纯文字卡片当封面
- 用架构图充当封面

## Stage 3: architecture diagram
使用 `scripts/render_arch_png.py`：
- 输入 `output/project_meta.json`
- 输入 `output/architecture_notes.md`
- 输出 `output/architecture-diagram.html`
- 输出 `images/arch.png`

## Stage 4: article
frontmatter 默认：
- author: 老夏的金库
- cover: cover.png

正文至少插入：
- `![GitHub项目截图](images/github_repo.png)`
- `![项目功能/README截图](images/github_readme.png)`
- `![项目架构图](images/arch.png)`

## Stage 5: preflight
未通过则禁止发布。校验：
- 封面是真实图
- 3 张正文图存在
- 架构图存在且非空
- author 正确
- 标题结构完整
- 有钩子 / Takeaway

## Stage 6: publish
默认 draft_only。
优先使用 Node 脚本发布。