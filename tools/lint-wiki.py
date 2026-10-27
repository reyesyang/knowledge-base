#!/usr/bin/env python3
"""只读的 wiki 体检工具（lint）。

用法：
    python3 tools/lint-wiki.py
    python3 tools/lint-wiki.py --verbose   # 同时列出全部页面清单

它检查 AGENTS.md §9 定义的若干项，输出问题清单，**不修改任何文件**。
发现问题后，由 agent 与用户确认再修。

退出码：0 = 无 error；1 = 存在 error。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
INDEX = ROOT / "index.md"
LOG = ROOT / "log.md"

TYPE_BY_DIR = {
    "sources": "source",
    "entities": "entity",
    "concepts": "concept",
    "comparisons": "comparison",
    "queries": "query",
    "synthesis": "synthesis",
}
REQUIRED_FIELDS = ["title", "type", "tags", "created", "updated", "sources", "status"]
VALID_STATUS = {"stable", "evolving", "draft"}

LINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
LOG_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \|", re.M)

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """极简 YAML frontmatter 解析：只处理本仓库用到的 `key: value` 标量行。"""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip("\n")
    body = text[end + 4 :]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data, body


def list_value(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [item.strip().strip("\"'") for item in raw.split(",") if item.strip()]


def link_target(raw: str) -> str:
    """`wiki/a.md|x` -> `wiki/a`；`a#标题` -> `a`。"""
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if target.endswith(".md"):
        target = target[:-3]
    return target


def load_pages() -> dict[str, dict]:
    pages: dict[str, dict] = {}
    if not WIKI.exists():
        return pages
    for path in sorted(WIKI.rglob("*.md")):
        rel = path.relative_to(ROOT).with_suffix("").as_posix()
        text = path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        pages[rel] = {
            "path": path,
            "rel": rel,
            "stem": path.stem,
            "meta": meta,
            "body": body,
            "text": text,
        }
    return pages


def strip_code(text: str) -> str:
    """去掉围栏代码块与行内代码。

    AGENTS.md 里大量 `[[sources/xxx]]` 只是语法示例，不能被当成真实链接去解析。
    """
    text = re.sub(r"^\s*(```|~~~).*?^\s*\1", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def read(path: Path) -> str:
    return strip_code(path.read_text(encoding="utf-8"))


def check_frontmatter(pages: dict[str, dict]) -> None:
    for rel, page in pages.items():
        meta = page["meta"]
        if not meta:
            err(f"缺少 frontmatter: {rel}")
            continue
        for field in REQUIRED_FIELDS:
            if field not in meta:
                err(f"frontmatter 缺字段 `{field}`: {rel}")
        status = meta.get("status", "").strip()
        if status and status not in VALID_STATUS:
            err(f"非法 status `{status}`: {rel}")
        expected = TYPE_BY_DIR.get(Path(rel).parent.name)
        if expected is None and rel == "wiki/overview":
            expected = "overview"
        actual = meta.get("type", "").strip()
        if expected and actual and actual != expected:
            err(f"type 与目录不符（应为 `{expected}`，实际 `{actual}`）: {rel}")
        if status == "draft":
            continue
        sources = list_value(meta.get("sources", ""))
        # source 页自身的依据是它引用的 raw/ 文件，不需要再指向别的 wiki 页
        if not sources and expected != "source" and rel != "wiki/overview":
            warn(f"status={status} 但没有 sources: {rel}")
        elif expected == "source" and "raw/" not in page["text"]:
            warn(f"source 页未标注原始文件（建议在正文写 `raw/<file>`）: {rel}")
        for src in sources:
            key = link_target(src)
            if key not in pages:
                err(f"sources 引用了不存在的页面 `{src}`: {rel}")


def root_docs() -> list[Path]:
    """根目录下也参与链接解析的文档（schema / 索引 / 日志 / 说明）。"""
    return [p for p in (ROOT / "AGENTS.md", INDEX, LOG, ROOT / "README.md") if p.exists()]


def collect_links(pages: dict[str, dict]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """返回 (入链表, 断链表)，二者均以 rel 为键。"""
    inbound: dict[str, set[str]] = {rel: set() for rel in pages}
    broken: dict[str, set[str]] = {}
    resolvable = set(pages) | {p.relative_to(ROOT).with_suffix("").as_posix() for p in root_docs()}

    for path in [page["path"] for page in pages.values()] + root_docs():
        rel = path.relative_to(ROOT).with_suffix("").as_posix()
        for raw in LINK_RE.findall(read(path)):
            target = link_target(raw)
            if not target:
                continue
            match = resolve(target, resolvable, pages, path)
            if match is None:
                broken.setdefault(rel, set()).add(raw)
            elif match in inbound and match != rel:
                inbound[match].add(rel)
    return inbound, broken


def resolve(target: str, resolvable: set[str], pages: dict[str, dict], current: Path) -> str | None:
    """把一个 wikilink 目标解析成页面 rel（或根文档 stem）。

    依次尝试：全路径 → 加 `wiki/` 前缀 → 裸文件名（stem）→ 相对当前文件。
    """
    if target in resolvable:
        return target
    if f"wiki/{target}" in resolvable:
        return f"wiki/{target}"
    for rel, page in pages.items():
        if page["stem"] == target:
            return rel
    try:
        rel_dir = current.parent.relative_to(ROOT).as_posix()
    except ValueError:
        rel_dir = "."
    candidate = target if rel_dir == "." else f"{rel_dir}/{target}"
    return candidate if candidate in resolvable else None


def check_links(pages: dict[str, dict]) -> None:
    inbound, broken = collect_links(pages)
    for rel, targets in broken.items():
        for target in sorted(targets):
            err(f"断链 [[{target}]]: {rel}")
    for rel, sources in inbound.items():
        if not sources and rel not in {"wiki/overview"}:
            warn(f"孤儿页（无入链）: {rel}")


def check_index(pages: dict[str, dict]) -> None:
    if not INDEX.exists():
        err("缺少 index.md")
        return
    text = read(INDEX)
    resolvable = set(pages) | {d.relative_to(ROOT).with_suffix('').as_posix() for d in root_docs()}
    resolved = set()
    for raw in LINK_RE.findall(text):
        match = resolve(link_target(raw), resolvable, pages, INDEX)
        if match in pages:
            resolved.add(match)
        elif match is None:
            err(f"index.md 中有断链 [[{raw}]]")
    for rel in pages:
        if rel != "wiki/overview" and rel not in resolved:
            warn(f"页面未登记到 index.md: {rel}")


def check_log() -> None:
    if not LOG.exists():
        err("缺少 log.md")
        return
    entries = LOG_RE.findall(LOG.read_text(encoding="utf-8"))
    if not entries:
        warn("log.md 中没有任何符合 `## [YYYY-MM-DD] type | title` 格式的条目")
    else:
        dates = [d for d, _ in entries]
        if dates != sorted(dates):
            warn("log.md 条目日期不是单调递增（只追加原则可能被破坏）")


def check_raw() -> None:
    raw = ROOT / "raw"
    if not raw.exists():
        warn("缺少 raw/ 目录")
        return
    files = [p for p in raw.rglob("*") if p.is_file()]
    if not files:
        warn("raw/ 为空 —— 还没有任何原始素材")


def main() -> int:
    parser = argparse.ArgumentParser(description="wiki 体检（只读）")
    parser.add_argument("--verbose", action="store_true", help="列出全部页面")
    args = parser.parse_args()

    if not WIKI.exists():
        print(f"找不到 wiki/ 目录：{WIKI}", file=sys.stderr)
        return 1

    pages = load_pages()
    check_frontmatter(pages)
    check_links(pages)
    check_index(pages)
    check_log()
    check_raw()

    print(f"扫描页面 {len(pages)} 个\n")

    if args.verbose:
        for rel in pages:
            print(f"  - {rel}")
        print()

    def dump(title: str, items: list[str], stream) -> None:
        print(f"{title}（{len(items)}）", file=stream)
        for item in items:
            print(f"  - {item}", file=stream)
        print(file=stream)

    if errors:
        dump("ERROR", errors, sys.stderr)
    if warnings:
        dump("WARN", warnings, sys.stderr)
    if not errors and not warnings:
        print("✓ 没有发现问题")
    print(f"结论：{len(errors)} error / {len(warnings)} warning")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
