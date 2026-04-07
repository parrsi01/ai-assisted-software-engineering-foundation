"""
Sample Capstone Project: CLI Expense Tracker

Usage:
    python main.py add --amount 12.50 --category food --note "lunch"
    python main.py list
    python main.py summary
    python main.py export expenses.csv
"""
import argparse
import json
import csv
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


DATA_FILE = Path("expenses.json")


def load_expenses() -> list[dict]:
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def save_expenses(expenses: list[dict]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def cmd_add(args) -> None:
    expenses = load_expenses()
    entry = {
        "id": len(expenses) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(args.amount, 2),
        "category": args.category.lower(),
        "note": args.note or "",
    }
    expenses.append(entry)
    save_expenses(expenses)
    print(f"Added: {entry['category']} ${entry['amount']:.2f} on {entry['date']}")


def cmd_list(args) -> None:
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
        return
    # Filter by category if specified
    if args.category:
        expenses = [e for e in expenses if e["category"] == args.category.lower()]
    print(f"{'ID':>4}  {'Date':<12}  {'Category':<15}  {'Amount':>8}  Note")
    print("-" * 60)
    for e in expenses:
        print(f"{e['id']:>4}  {e['date']:<12}  {e['category']:<15}  ${e['amount']:>7.2f}  {e['note']}")
    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal: ${total:.2f}")


def cmd_summary(args) -> None:
    expenses = load_expenses()
    if not expenses:
        print("No expenses.")
        return
    by_category: dict[str, float] = defaultdict(float)
    by_month: dict[str, float] = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]
        month = e["date"][:7]  # YYYY-MM
        by_month[month] += e["amount"]

    print("=== By Category ===")
    for cat, total in sorted(by_category.items()):
        print(f"  {cat:<20} ${total:>8.2f}")

    print("\n=== By Month ===")
    for month, total in sorted(by_month.items()):
        print(f"  {month:<20} ${total:>8.2f}")

    grand_total = sum(e["amount"] for e in expenses)
    print(f"\nGrand Total: ${grand_total:.2f}")


def cmd_export(args) -> None:
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return
    output = Path(args.file)
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category", "note"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Exported {len(expenses)} expenses to {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add an expense")
    add_p.add_argument("--amount", type=float, required=True)
    add_p.add_argument("--category", required=True)
    add_p.add_argument("--note", default="")

    list_p = sub.add_parser("list", help="List expenses")
    list_p.add_argument("--category", help="Filter by category")

    sub.add_parser("summary", help="Summary by category and month")

    export_p = sub.add_parser("export", help="Export to CSV")
    export_p.add_argument("file", help="Output CSV filename")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "summary": cmd_summary,
        "export": cmd_export,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
