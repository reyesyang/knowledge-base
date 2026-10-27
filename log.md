# 日志

> 只追加，不改写历史（写错就在下一条里更正）。格式：`## [YYYY-MM-DD] 类型 | 摘要`
> 类型：`ingest` / `query` / `lint` / `schema` / `refactor` / `note`
> 快速查看：`grep "^## \[" log.md | tail -5`

## [2026-10-26] schema | 初始化 LLM Wiki 骨架与 AGENTS.md
- 建立三层结构：`raw/`（不可变素材）+ `wiki/`（LLM 独占）+ `AGENTS.md`（schema）
- 创建目录：`raw/assets`、`wiki/{sources,entities,concepts,comparisons,queries,synthesis}`
- 制定规范：frontmatter 字段、kebab-case 命名、扁平优先、`index.md` 内容索引、`log.md` 时间线日志
- 定义四类操作：ingest / query / lint / refactor
- 依据：Karpathy《LLM Wiki》gist `442a6bf555914893e9891c11519de94f`
- 决策：vault 根即知识库根（单 vault）；初期不预设领域分类，采用通用四类

## [2026-10-26] ingest | Karpathy《LLM Wiki》
- 原始素材：`raw/karpathy-llm-wiki.md`（gist 原文，75 行）
- 新增：[[wiki/sources/karpathy-llm-wiki]]
- 新增：[[wiki/concepts/llm-wiki]]、[[wiki/concepts/rag]]、[[wiki/comparisons/llm-wiki-vs-rag]]、[[wiki/overview]]
- 新增工具：`tools/lint-wiki.py`（只读体检脚本）
- 说明：以方法论原文本身作为第一份素材，用于验证 ingest 流程可用
- 矛盾：无
- 后续：待用户投入第一批真实素材后再细化 tags 体系与实体分类

## [2026-10-27] schema | 新增 §7 标准工作流总览，章节重编号 7–14 → 8–15
- 动机：四类操作分散在各自小节，缺少把流程串起来的一处总览
- 新增：§7 标准工作流总览（会话启动图、四操作对照表、各操作的"完成"标准、节奏建议、最小可运行循环）
- 调整：原 §7–§14 顺延为 §8–§15；同步修正 §1、§7、§12 内的交叉引用
- 未改动：目录结构、frontmatter 规范、链接约定
