#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

DATA_FILE = Path("data/ledger.json")


@dataclass
class Entry:
    id: int
    kind: str
    amount: float
    category: str
    entry_date: str
    note: str = ""


def load_entries() -> list[Entry]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    entries: list[Entry] = []
    for i, item in enumerate(raw, start=1):
        item = dict(item)
        item.setdefault("id", i)
        entries.append(Entry(**item))
    return entries


def save_entries(entries: list[Entry]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps([asdict(e) for e in entries], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def next_id(entries: list[Entry]) -> int:
    return max((e.id for e in entries), default=0) + 1


def cmd_add(args: argparse.Namespace) -> None:
    entries = load_entries()
    entry = Entry(
        id=next_id(entries),
        kind=args.kind,
        amount=round(args.amount, 2),
        category=args.category,
        entry_date=args.date or date.today().isoformat(),
        note=args.note or "",
    )
    entries.append(entry)
    save_entries(entries)
    print(f"已记录 #{entry.id}：{entry.kind} ¥{entry.amount:.2f} / {entry.category} / {entry.entry_date}")


def cmd_list(args: argparse.Namespace) -> None:
    entries = load_entries()
    month = args.month
    if month:
        entries = [e for e in entries if e.entry_date.startswith(month)]
    if not entries:
        print("暂无记录。")
        return
    print("ID  日期       类型     金额      分类        备注")
    print("-" * 64)
    for e in entries:
        print(f"{e.id:<3} {e.entry_date}  {e.kind:<7} {e.amount:>8.2f}  {e.category:<10}  {e.note}")


def calc_summary(entries: list[Entry]) -> tuple[float, float, float]:
    income = sum(e.amount for e in entries if e.kind == "income")
    expense = sum(e.amount for e in entries if e.kind == "expense")
    return income, expense, income - expense


def cmd_summary(args: argparse.Namespace) -> None:
    entries = load_entries()
    if args.month:
        entries = [e for e in entries if e.entry_date.startswith(args.month)]
        print(f"月份: {args.month}")
    income, expense, balance = calc_summary(entries)
    print(f"总收入: ¥{income:.2f}")
    print(f"总支出: ¥{expense:.2f}")
    print(f"结余:   ¥{balance:.2f}")


def cmd_category(args: argparse.Namespace) -> None:
    entries = load_entries()
    if args.month:
        entries = [e for e in entries if e.entry_date.startswith(args.month)]
        print(f"月份: {args.month}")

    expense_by_category: dict[str, float] = {}
    for e in entries:
        if e.kind != "expense":
            continue
        expense_by_category[e.category] = expense_by_category.get(e.category, 0.0) + e.amount

    if not expense_by_category:
        print("暂无支出分类数据。")
        return

    print("分类支出统计：")
    for cat, amount in sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"- {cat}: ¥{amount:.2f}")


def cmd_delete(args: argparse.Namespace) -> None:
    entries = load_entries()
    kept = [e for e in entries if e.id != args.id]
    if len(kept) == len(entries):
        print(f"未找到 ID={args.id} 的记录。")
        return
    save_entries(kept)
    print(f"已删除 ID={args.id} 的记录。")


def cmd_health(_: argparse.Namespace) -> None:
    entries = load_entries()
    print("=== 仓库阶段检查（记账项目）===")
    print(f"记录总数: {len(entries)}")
    print(f"数据文件: {DATA_FILE} ({'存在' if DATA_FILE.exists() else '不存在'})")
    required = ["README.md", "app.py", ".gitignore"]
    for f in required:
        print(f"- {f}: {'OK' if Path(f).exists() else '缺失'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="个人记账工具（CLI）")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="新增一条收支记录")
    add.add_argument("kind", choices=["income", "expense"], help="收入或支出")
    add.add_argument("amount", type=float, help="金额")
    add.add_argument("category", help="分类，例如 餐饮/工资")
    add.add_argument("--date", help="日期，格式 YYYY-MM-DD")
    add.add_argument("--note", help="备注")
    add.set_defaults(func=cmd_add)

    show = sub.add_parser("list", help="查看记录")
    show.add_argument("--month", help="按月份筛选，例如 2026-05")
    show.set_defaults(func=cmd_list)

    summary = sub.add_parser("summary", help="查看汇总")
    summary.add_argument("--month", help="按月份筛选，例如 2026-05")
    summary.set_defaults(func=cmd_summary)

    category = sub.add_parser("category", help="查看分类支出统计")
    category.add_argument("--month", help="按月份筛选，例如 2026-05")
    category.set_defaults(func=cmd_category)

    delete = sub.add_parser("delete", help="按 ID 删除一条记录")
    delete.add_argument("id", type=int, help="记录 ID")
    delete.set_defaults(func=cmd_delete)

    health = sub.add_parser("health", help="做一次阶段检查（库存/合规基础项）")
    health.set_defaults(func=cmd_health)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
