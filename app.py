#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

DATA_FILE = Path("data/ledger.json")


@dataclass
class Entry:
    kind: str
    amount: float
    category: str
    entry_date: str
    note: str = ""


def load_entries() -> list[Entry]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Entry(**item) for item in raw]


def save_entries(entries: list[Entry]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps([asdict(e) for e in entries], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def cmd_add(args: argparse.Namespace) -> None:
    entries = load_entries()
    entry = Entry(
        kind=args.kind,
        amount=round(args.amount, 2),
        category=args.category,
        entry_date=args.date or date.today().isoformat(),
        note=args.note or "",
    )
    entries.append(entry)
    save_entries(entries)
    print(f"已记录：{entry.kind} ¥{entry.amount:.2f} / {entry.category} / {entry.entry_date}")


def cmd_list(_: argparse.Namespace) -> None:
    entries = load_entries()
    if not entries:
        print("暂无记录。")
        return
    print("日期       类型   金额      分类        备注")
    print("-" * 50)
    for e in entries:
        print(f"{e.entry_date}  {e.kind:<4}  {e.amount:>8.2f}  {e.category:<10}  {e.note}")


def cmd_summary(_: argparse.Namespace) -> None:
    entries = load_entries()
    income = sum(e.amount for e in entries if e.kind == "income")
    expense = sum(e.amount for e in entries if e.kind == "expense")
    balance = income - expense
    print(f"总收入: ¥{income:.2f}")
    print(f"总支出: ¥{expense:.2f}")
    print(f"结余:   ¥{balance:.2f}")


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

    show = sub.add_parser("list", help="查看全部记录")
    show.set_defaults(func=cmd_list)

    summary = sub.add_parser("summary", help="查看汇总")
    summary.set_defaults(func=cmd_summary)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
