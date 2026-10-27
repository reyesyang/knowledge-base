---
title: RAG（检索增强生成）
type: concept
tags: [llm, retrieval, architecture]
created: 2026-10-26
updated: 2026-10-26
sources: [wiki/sources/karpathy-llm-wiki.md]
status: evolving
aliases: [Retrieval-Augmented Generation, 检索增强, RAG]
---

# RAG（检索增强生成）

在提问时从原始文档中检索相关片段，再交给 LLM 生成答案的范式。它的优点是无需预先整理、覆盖面大；
代价是**每次提问都从零重新推导**，知识不会积累。它是 [[concepts/llm-wiki]] 要对照的基线。

## 定义

典型链路：文档切块 → 建索引（向量 / BM25 / 混合）→ 按问题检索 top-k 片段 → 拼进上下文 → 生成答案。
代表性产品：NotebookLM、ChatGPT 文件上传，以及绝大多数企业知识库问答。

## 结构性局限（本 wiki 记录的视角）

- **没有积累**：同一主题被问十次，就重建十次；每次的结论可能不一致。
- **综合能力被切块打散**：需要跨越五份文档的细微问题，每次都要重新找齐片段并临场拼接。
- **矛盾不会被发现**：两份文档抵触时，检索通常只是把两段一起塞进上下文，由模型临场取舍。
- **关系不可见**：不存在一张持续维护的图，谁引用了谁、哪里被新证据推翻，都无从体现。

> 注：以上是 [[sources/karpathy-llm-wiki]] 提出的对照性批评，**不是**对 RAG 适用范围的全面评估。
> RAG 在"海量、少读、随时新增"的场景仍更经济 —— 这也是本页 `status: evolving` 的原因：
> 待补充 RAG 一方更完整的辩护与适用边界。

## 与 LLM Wiki 的关系

两者并不互斥：Wiki 是"把阅读成果编译成人可读的结构化资产"，RAG 是"在原始语料上做运行时检索"。
规模小时 Wiki 更划算（人可读、可审计、可 diff）；语料巨大且只读一次时 RAG 更划算。
详见 [[comparisons/llm-wiki-vs-rag]]。

## 未解问题

- 混合方案是否最优：wiki 层做"已消化知识"，RAG 兜底"未消化语料"？
- 当 wiki 到达 index.md 不再够用的规模，引入向量检索是否就等于退化回 RAG，还是变成"检索 wiki"？
