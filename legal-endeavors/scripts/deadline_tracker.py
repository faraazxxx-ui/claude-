#!/usr/bin/env python3
"""
Deadline Tracker for Rahman v. UHS et al.
Case No. 3:26-CV-00197 (AJB/ML)

Usage:
    python3 deadline_tracker.py                  # Show all deadlines
    python3 deadline_tracker.py --urgent          # Show only urgent (within 30 days)
    python3 deadline_tracker.py --add "Description" "YYYY-MM-DD" "Category"
    python3 deadline_tracker.py --json            # Output as JSON
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

DEADLINES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "deadlines.json")

DEFAULT_DEADLINES = [
    {
        "description": "Malicious Prosecution SOL (1 year from acquittal)",
        "date": "2026-08-31",
        "category": "statute_of_limitations",
        "status": "pending",
        "notes": "Must file malicious prosecution claim before this date. Acquittal was August 2025."
    },
    {
        "description": "EEOC Charge Filing (300 days from last discriminatory act)",
        "date": "2026-05-15",
        "category": "administrative",
        "status": "verify",
        "notes": "Verify if EEOC charge has been filed. Last discriminatory act may be July 2024 (record obstruction)."
    },
    {
        "description": "Rule 26(f) Conference Preparation",
        "date": "2026-04-30",
        "category": "litigation",
        "status": "pending",
        "notes": "Prepare initial disclosures and discovery plan. Defendants answered March 9, 2026."
    },
    {
        "description": "Initial Disclosures Due",
        "date": "2026-05-15",
        "category": "litigation",
        "status": "pending",
        "notes": "14 days after Rule 26(f) conference per FRCP 26(a)(1)."
    },
    {
        "description": "Motion to Compel Email Access",
        "date": "2026-04-30",
        "category": "motion",
        "status": "pending",
        "notes": "File early to recover Plaintiff's UHS email archive."
    },
    {
        "description": "Amended Complaint (add Sundas, ADA, Title VII claims)",
        "date": "2026-06-30",
        "category": "litigation",
        "status": "pending",
        "notes": "Amend as of right within 21 days of service, or seek leave of court."
    }
]


def load_deadlines():
    if os.path.exists(DEADLINES_FILE):
        with open(DEADLINES_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DEADLINES


def save_deadlines(deadlines):
    os.makedirs(os.path.dirname(DEADLINES_FILE), exist_ok=True)
    with open(DEADLINES_FILE, "w") as f:
        json.dump(deadlines, f, indent=2)


def days_until(date_str):
    target = datetime.strptime(date_str, "%Y-%m-%d")
    delta = target - datetime.now()
    return delta.days


def display_deadlines(deadlines, urgent_only=False, as_json=False):
    today = datetime.now()
    sorted_deadlines = sorted(deadlines, key=lambda d: d["date"])

    if urgent_only:
        sorted_deadlines = [d for d in sorted_deadlines if days_until(d["date"]) <= 30]

    if as_json:
        for d in sorted_deadlines:
            d["days_remaining"] = days_until(d["date"])
        print(json.dumps(sorted_deadlines, indent=2))
        return

    print(f"\n{'='*80}")
    print(f"  DEADLINE TRACKER — Rahman v. UHS et al. (3:26-CV-00197)")
    print(f"  As of: {today.strftime('%B %d, %Y')}")
    print(f"{'='*80}\n")

    for d in sorted_deadlines:
        days = days_until(d["date"])
        if days < 0:
            urgency = "OVERDUE"
        elif days <= 7:
            urgency = "CRITICAL"
        elif days <= 30:
            urgency = "URGENT"
        elif days <= 90:
            urgency = "UPCOMING"
        else:
            urgency = "SCHEDULED"

        print(f"  [{urgency}] {d['description']}")
        print(f"           Date: {d['date']}  |  Days: {days}  |  Category: {d['category']}  |  Status: {d['status']}")
        if d.get("notes"):
            print(f"           Note: {d['notes']}")
        print()

    print(f"{'='*80}")
    print(f"  Total deadlines: {len(sorted_deadlines)}")
    overdue = sum(1 for d in sorted_deadlines if days_until(d["date"]) < 0)
    critical = sum(1 for d in sorted_deadlines if 0 <= days_until(d["date"]) <= 7)
    urgent = sum(1 for d in sorted_deadlines if 7 < days_until(d["date"]) <= 30)
    if overdue:
        print(f"  OVERDUE: {overdue}")
    if critical:
        print(f"  CRITICAL (<=7 days): {critical}")
    if urgent:
        print(f"  URGENT (<=30 days): {urgent}")
    print(f"{'='*80}\n")


def add_deadline(description, date, category, notes=""):
    deadlines = load_deadlines()
    deadlines.append({
        "description": description,
        "date": date,
        "category": category,
        "status": "pending",
        "notes": notes
    })
    save_deadlines(deadlines)
    print(f"Added deadline: {description} ({date})")


def main():
    parser = argparse.ArgumentParser(description="Deadline Tracker for Rahman v. UHS")
    parser.add_argument("--urgent", action="store_true", help="Show only urgent deadlines (within 30 days)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--add", nargs=3, metavar=("DESC", "DATE", "CATEGORY"), help="Add a new deadline")
    parser.add_argument("--notes", default="", help="Notes for new deadline (use with --add)")
    parser.add_argument("--init", action="store_true", help="Initialize deadlines file with defaults")
    args = parser.parse_args()

    if args.init:
        save_deadlines(DEFAULT_DEADLINES)
        print(f"Initialized deadlines file at {DEADLINES_FILE}")
        return

    if args.add:
        add_deadline(args.add[0], args.add[1], args.add[2], args.notes)
        return

    deadlines = load_deadlines()
    display_deadlines(deadlines, urgent_only=args.urgent, as_json=args.json)


if __name__ == "__main__":
    main()
