---
title: Karpathy《LLM Wiki》
type: source
tags: [methodology, knowledge-management, llm, prompt]
created: 2026-10-26
updated: 2026-10-26
sources: []
status: stable
aliases: [LLM Wiki, karpathy llm wiki, 442a6bf5]
---

# Karpathy《LLM Wiki》

- **原始素材**：`raw/karpathy-llm-wiki.md`（2026-10-26 从 gist raw 地址抓取的完整原文，75 行）
  - 出处：<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
  - 类型：概念性设计文档（"idea file"，明确说明供直接粘贴给自己的 LLM Agent）
  - 作者 / 时间：Andrej Karpathy / 2026-04（按 gist 上下文）
- **一句话结论**：不要让 LLM 在每次提问时从原始文档重新检索推导；让它**增量构建并维护一个持久的、
  交叉引用的 markdown wiki**，知识"编译一次、持续保鲜"，从而随每个新素材和每次提问而复利增长。

## 关键要点

1. **对照对象是 RAG**。RAG（含 NotebookLM、ChatGPT 文件上传类）每次提问都重新找片段、重新拼答案，
   没有积累；需要综合五份文档的细微问题，每次都要重做一遍。见 [[concepts/rag]]。
2. **三层架构**：① 原始素材（不可变，source of truth）② wiki（LLM 独占生成的 markdown 层）
   ③ schema（`AGENTS.md` / `CLAUDE.md`，定义结构、约定、工作流）。schema 是让 LLM 成为
   "守规矩的 wiki 维护者"而非通用聊天机器人的关键配置。见 [[concepts/llm-wiki]]。
3. **分工反直觉但清晰**：人类负责选素材、探索、提问、判断意义；LLM 负责全部苦力活
   ——摘要、交叉引用、归档、记账、一致性。人类几乎不亲手写 wiki。
4. **四类操作**：Ingest（摄入，一份素材可触及 10–15 个页面）、Query（提问，好的答案要**回写**进 wiki）、
   Lint（体检：矛盾、陈旧、孤儿页、断链、缺口）、以及隐含的 Refactor。
5. **两个特殊文件职责分离**：`index.md` 面向内容（分类目录，每次 ingest 更新，查询时先读它，
   在 ~100 源 / 数百页规模下足以替代向量检索）；`log.md` 面向时间（只追加，固定前缀
   `## [日期] 类型 | 标题` 使日志可被 unix 工具解析）。
6. **为什么有效**：知识库的真正成本不是阅读思考，而是记账式维护（更新交叉引用、保持摘要新鲜、
   标注矛盾）。人类放弃 wiki 是因为维护成本增长快于价值；LLM 不厌倦、不会漏改、一次能改 15 个文件。
7. **它明确是抽象文档**：目录结构、页面格式、工具（qmd 搜索、Obsidian Web Clipper、Marp、Dataview、
   图谱视图、本地图片下载）全都可选、可模块化，具体实现由用户与 agent 共同敲定。

## 可复用的事实 / 数据

- 单份素材摄入预期影响 **10–15** 个 wiki 页面（这是"整合"而非"索引"的量化体现）。
- `index.md` 路线在 **~100 个源、数百个页面**的规模内依然够用，无需 embedding/RAG 基础设施。
- 推荐的工作节奏：**一次一份、人在环中**（读摘要、看更新、引导侧重），批量摄入是可选变体。
- 类比：Obsidian = IDE，LLM = 程序员，wiki = 代码库；思想源头可追到 Vannevar Bush 的 Memex (1945)。
- 适用场景：个人成长追踪、长期研究、读书伴读 wiki（对标 Tolkien Gateway）、团队内部 wiki 等。

## 对既有 wiki 的影响

- **新增**：本仓库的整套骨架即由这份素材直接实例化而来 —— 见 [[concepts/llm-wiki]]、
  [[comparisons/llm-wiki-vs-rag]]、[[AGENTS]]。
- **佐证**：本仓库选择"通用起步、不预设领域分类"符合原文"具体实现依赖你的领域与偏好"的立场。
- **偏离（有意）**：原文说 schema 可以是 `CLAUDE.md` 或 `AGENTS.md`；本仓库统一用 `AGENTS.md`
  以获得跨工具通用性。
- **矛盾**：无。
