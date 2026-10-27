---
title: LLM Wiki vs RAG
type: comparison
tags: [methodology, retrieval, architecture]
created: 2026-10-26
updated: 2026-10-26
sources: [wiki/sources/karpathy-llm-wiki.md]
status: evolving
aliases: [wiki vs rag, 检索 vs 编译]
---

# LLM Wiki vs RAG

两种用 LLM 消费知识库的方式：**查询时检索**（RAG）vs **摄入时编译**（LLM Wiki）。
一句话：RAG 每次重新推导，wiki 一次编译持续保鲜；代价是前者零维护、后者需要 disciplined 的维护者
（而这正是 LLM 擅长的部分）。

## 对比表

| 维度 | RAG（检索即用） | LLM Wiki（编译即存） |
|---|---|---|
| 知识何时"成型" | 提问时（运行时） | 摄入时（写入时） |
| 成本主要在 | 每次查询都要检索 + 重读片段 | 一次摄入扩散改 10–15 页 |
| 是否积累 | 不积累，每次从零 | 持续复利 |
| 跨文档综合 | 临场拼接，质量取决于检索命中 | 已预先写好，随时可读 |
| 矛盾处理 | 通常无感知，交给模型临场取舍 | 显式标注、留痕、可追溯 |
| 人际可读性 | 无中间产物，只有答案 | 整套 wiki 人可读、可 diff、可审查 |
| 素材新增成本 | 极低（丢进去即可） | 中（需要一次达标摄入） |
| 规模适应 | 语料巨大时更经济 | ~100 源 / 数百页内最舒服 |
| 失效模式 | 检索不到 / 片段错位 / 答案不稳定 | 维护漂移 / 无来源的内容 / 过度设计 |
| 需要的基础设施 | 切块 + 向量库 / BM25 | 一个 git 仓库 + 一份 schema |

## 怎么选

- **要"越用越厚的资产"**（研究、读书、个人长期追踪、团队内部知识）→ LLM Wiki。你的问题会越来越深，
  而深度来自积累，不来自更强的检索。
- **要"海量语料的即时问答"**（客服、法务检索、一次性的资料排查）→ RAG。没人会去维护几万页 wiki。
- **语料中等、且你会反复问同类问题** → LLM Wiki 优先；`index.md` 在小规模下比向量检索更可靠。
- **折中方案**：wiki 沉淀"已消化的结论"，RAG 兜底"未消化的原始语料"。
  本仓库目前只做前者，规模变大时再考虑引入搜索（见 [[AGENTS]] §12）。

## 需要注意的偏差

本页的 RAG 一列主要来自 [[sources/karpathy-llm-wiki]] 的对照性论述，倾向于强调 wiki 的优势。
若要做严肃选型，应补充 RAG 侧在超大规模与少读场景的实证数据。因此本页标为 `status: evolving`。

## 相关

- [[concepts/llm-wiki]]、[[concepts/rag]]、[[wiki/overview|overview]]
