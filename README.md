# 知识库（LLM Wiki）

一个由 LLM 增量维护的个人知识库，遵循 Karpathy 的 **LLM Wiki** 方法论：
原始素材进来后不只被索引，而是被**整合**进一套互相链接的 markdown 页面，知识因此持续累积。

- 方法论出处：<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- 仓库内的方法论笔记：[[wiki/concepts/llm-wiki]]

## 三层结构

```
raw/     原始素材（不可变，LLM 只读）
wiki/    LLM 生成并维护的页面
AGENTS.md  schema —— 告诉 LLM 怎么干活的规范文件
```

## 怎么用

**用 Obsidian 打开这个目录**（vault 根 = 仓库根），左侧浏览 wiki，右侧让 LLM agent 干活。
Obsidian 是 IDE，agent 是程序员，wiki 是代码库。

推荐一次性设置：
1. 设置 → 文件与链接 → 附件默认位置 → 填 `raw/assets`
2. 设置 → 快捷键 → 搜索 "Download" → 绑定"下载当前文件的附件"（Ctrl/Cmd+Shift+D），
   抓文章后一键把图片存到本地
3. 打开图谱视图观察 hub 与孤儿页
4. 可选插件：Dataview（基于 frontmatter 出动态表）、Marp（出幻灯片）

## 日常操作（对 agent 说这些就行）

| 你说 | agent 做什么 |
|---|---|
| "把 `raw/xxx.md` 摄入" | 读素材 → 讨论要点 → 写 source 页 → 扩散更新 3–15 个页面 → 更新 index 与 log |
| "问：……" | 先读 `index.md` 定位 → 读相关页 → 带引用的回答；有新增综合就回写 |
| "体检查一下" | 查矛盾、陈旧、孤儿页、断链、缺口 → 出报告（先不改） |

完整规则见 [AGENTS.md](AGENTS.md)（也是给所有 agent 用的入口）。

## 导航入口

- [index.md](index.md) — 全部页面索引
- [log.md](log.md) — 时间线日志（`grep "^## \[" log.md | tail -5`）
- [wiki/overview.md](wiki/overview.md) — 全局认知地图

## 体检

```bash
python3 tools/lint-wiki.py
```

## 版本控制

这就是一个 markdown git 仓库，历史与分支免费获得。
