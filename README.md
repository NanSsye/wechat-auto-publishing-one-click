# 微信公众号自动发文一键 Skill

一个面向 Hermes 的“开箱即用”技能包。

目标很直接：
- 只装这一个 Skill
- 单个 cron 内跑完整流程
- 自动选题、调研、配图、画架构图、写文章、校验、发草稿
- 不再额外依赖 `architecture-diagram`、`orchestrator` 之类外部 Skill 才能工作

---

## 这是什么

这是我把“公众号自动发文”这套流程，重新打包成的一个独立 Skill：

`wechat-auto-publishing-one-click`

它把下面这些能力都放进来了：

- GitHub 选题研究
- 子 Agent 并行调研模板
- Twitter / GitHub 真实素材抓取规则
- 真实封面规则
- 架构图 PNG 生成
- 中文公众号文章模板
- preflight 发布前校验
- 草稿发布模板
- bootstrap 自举脚本

---

## 适合谁

适合这几类人：

1. 想做“AI / 开源项目解读”公众号的人
2. 已经在用 Hermes，希望把发文流程自动化的人
3. 不想手动拼装一堆 Skill、脚本、规则的人
4. 想把整个流程分享给别人，降低上手门槛的人

---

## 这个 Skill 能做什么

单次运行里，默认按下面这条链路执行：

1. 初始化工作区
2. 并行调研候选项目
3. 收集真实用户反馈
4. 准备 GitHub / README / Twitter 真实图片
5. 生成项目架构图 PNG
6. 写成公众号文章
7. 做发布前校验
8. 发布到微信公众号草稿箱

也就是说，它不是“帮你写一段文案”，而是完整的“内容生产流水线”。

---

## 关键约束

这套 Skill 有几个硬规则：

- 封面不能用 AI 生图
- 封面必须来自 GitHub 或 Twitter/X 的真实项目图片/截图
- 架构图最终产物必须是 PNG
- 必须在一个 cron 任务里完成，不拆多段定时任务
- 作者名默认固定为：`老夏的金库`
- 默认发布模式是：`draft_only`

这些规则不是装饰，是为了保证最终成品更像“真公众号文章”，而不是测试稿。

---

## 目录结构

仓库里最核心的部分是：

```text
wechat-auto-publishing-one-click/
├── SKILL.md
├── assets/
│   └── architecture_template.html
├── references/
│   ├── assets.md
│   ├── publishing.md
│   ├── runbook.md
│   ├── share-readme.md
│   └── workflow.md
├── scripts/
│   ├── bootstrap.sh
│   ├── make_real_cover.py
│   └── render_arch_png.py
└── templates/
    ├── article-template.md
    ├── cron_prompt.txt
    ├── env.example.txt
    └── publish.mjs
```

---

## 安装方式

把整个目录复制到 Hermes skills 目录：

```bash
cp -r wechat-auto-publishing-one-click ~/.hermes/skills/
```

然后运行自举脚本：

```bash
cd ~/.hermes/skills/wechat-auto-publishing-one-click
bash scripts/bootstrap.sh
```

---

## 需要的环境

建议机器至少具备：

- `python3`
- `node`
- `npm`
- `chromium` 或可被 Playwright 调起的浏览器

bootstrap 会尽量帮你补：

- `pillow`
- `playwright`
- `cairosvg`
- `pyyaml`
- `requests`

但是否能成功安装，还是取决于你的系统环境。

---

## 配置方式

参考：

```text
templates/env.example.txt
```

你至少要准备自己的：

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`

注意：

不要把真实凭据提交进仓库。

---

## 怎么接到 Hermes cron

最简单的方式：

直接把下面这个文件内容，当成 cron prompt：

```text
templates/cron_prompt.txt
```

然后在 Hermes 里创建一个单 cron 任务，让它一次跑完整流程。

---

## 生成的关键产物

正常跑完后，至少应该看到这些文件：

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

如果这些不齐，说明流程没真正走完。

---

## 为什么要单独做架构图 PNG

很多“自动发文”方案，最后都停在“有文字、没结构”。

我这里把架构图单独做成一个明确阶段，而且强制输出 PNG，是因为：

- PNG 更适合直接嵌入公众号正文
- 比纯 HTML 中间产物更稳定
- 更容易做 preflight 校验
- 也更符合真正发布时的素材需求

脚本在这里：

```bash
python3 scripts/render_arch_png.py \
  --meta output/project_meta.json \
  --notes output/architecture_notes.md \
  --html output/architecture-diagram.html \
  --png images/arch.png
```

---

## 为什么封面禁止 AI 生图

因为 AI 生成封面虽然快，但很容易“假、空、泛”。

真正适合公众号封面的，往往还是：

- GitHub README 图
- 项目 Dashboard 截图
- 官方功能图
- Twitter / X 上项目相关真实截图

所以这个 Skill 里明确规定：

- 不允许 AI 生图当封面
- 不允许纯文字卡片当封面
- 不允许直接把架构图拿去当封面

封面处理脚本：

```bash
python3 scripts/make_real_cover.py \
  --input images/github_repo.png \
  --fallback images/github_readme.png \
  --output cover.png
```

---

## 成功标准

只有同时满足这些，才算真正成功：

- 已完成并行调研
- 已拿到真实项目图
- 已生成真实封面
- 已生成架构图 PNG
- `article.md` 已写出
- `preflight` 通过
- 微信草稿创建成功

也就是说，不是“能发出去就算赢”，而是“成品质量过线才算赢”。

---

## 如果你要分享给别人

最推荐的方式就是：

1. 分享这个 GitHub 仓库
2. 让对方复制 Skill 到 `~/.hermes/skills/`
3. 跑 `bootstrap.sh`
4. 配好 `.env`
5. 把 `templates/cron_prompt.txt` 接进 Hermes cron

这样别人不用再自己一点点拼。

---

## 当前状态

这个仓库现在已经是一个“可分享、可复用、可继续迭代”的版本。

它不保证在所有机器上 100% 零配置成功，
但已经把最麻烦的那部分——流程、规则、脚本、模板——全部收进来了。

如果你也在做 Hermes 的公众号自动化，这个仓库应该能直接省掉你一大半折腾时间。

---

## 仓库地址

```text
https://github.com/NanSsye/wechat-auto-publishing-one-click
```

如果这个 Skill 对你有帮助，点个 Star 就行。