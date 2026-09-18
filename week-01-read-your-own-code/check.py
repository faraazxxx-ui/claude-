#!/usr/bin/env python3
"""
Week 01 verifier.

Grades your edited specimen.py pass/fail, one line per requirement.
It does not show you the answer and it does not care how you got there.

    python3 check.py

Design note: the thing that grades the work is not the thing that did the work.
That is the whole reason this file is separate from specimen.py.
"""

import io
import os
import re
import sys
import contextlib

PASS = "PASS"
FAIL = "FAIL"
results = []


def line(status, label, detail=""):
    results.append((status, label, detail))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    sys.path.insert(0, here)

    # --- import the specimen -------------------------------------------------
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import specimen
    except PermissionError as exc:
        line(FAIL, "specimen.py can be imported",
             f"permission denied: {exc}. A path constant still points somewhere "
             "you are not allowed to write.")
        return report()
    except Exception as exc:
        line(FAIL, "specimen.py can be imported", f"{type(exc).__name__}: {exc}")
        return report()
    line(PASS, "specimen.py can be imported")

    # --- input paths ---------------------------------------------------------
    upload = getattr(specimen, "UPLOAD_DIR", None)
    if upload and os.path.isdir(upload):
        line(PASS, "UPLOAD_DIR points at a directory that exists")
    else:
        line(FAIL, "UPLOAD_DIR points at a directory that exists",
             f"got {upload!r}")

    found = []
    if upload and os.path.isdir(upload):
        found = [f for f in os.listdir(upload) if f.lower().endswith(".csv")]
    if len(found) >= 2:
        line(PASS, "both CSVs are reachable from UPLOAD_DIR",
             f"{len(found)} csv files")
    else:
        line(FAIL, "both CSVs are reachable from UPLOAD_DIR",
             f"found {len(found)}")

    # --- run it --------------------------------------------------------------
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            specimen.main()
        line(PASS, "specimen.main() runs without raising")
    except Exception as exc:
        line(FAIL, "specimen.main() runs without raising",
             f"{type(exc).__name__}: {exc}")
        return report()

    # --- inspect what it wrote ----------------------------------------------
    out = getattr(specimen, "OUTPUT_FILE", None)
    if not (out and os.path.isfile(out)):
        line(FAIL, "the report file exists", f"expected at {out!r}")
        return report()
    line(PASS, "the report file exists")

    text = open(out, encoding="utf-8").read()

    if "not found" in text.lower():
        line(FAIL, "report contains no 'not found' placeholder",
             "a section is still returning the apology string instead of a table")
    else:
        line(PASS, "report contains no 'not found' placeholder")

    dates = re.findall(r"\b20\d{2}-\d{2}-\d{2}\b", text)
    if len(dates) >= 50:
        line(PASS, "report contains real dated rows", f"{len(dates)} dates")
    else:
        line(FAIL, "report contains real dated rows",
             f"only {len(dates)} dates found")

    tables = text.count("|---")
    if tables >= 2:
        line(PASS, "both tables rendered", f"{tables} markdown tables")
    else:
        line(FAIL, "both tables rendered", f"{tables} found, expected 2")

    failed = report()

    # --- observation, not a grade -------------------------------------------
    # Sitting 3 has two defensible answers. Recording which one you took is not
    # the same as scoring it, so this sits below the rubric, not inside it.
    # It only means anything once the report actually has data in it.
    if not failed:
        if "In Bed" in text:
            note = ("You kept in-bed time. Be able to say how you reconstructed "
                    "it and which night it failed to reconcile.")
        else:
            note = ("You dropped in-bed time. Be able to say what that costs "
                    "you when you next interpret sleep efficiency.")
        print(f"Sitting 3 — your call: {note}\n")

    return failed


def report():
    width = max(len(label) for _, label, _ in results)
    print()
    for status, label, detail in results:
        mark = "✓" if status == PASS else "✗"
        print(f"  {mark} {status}  {label.ljust(width)}"
              + (f"   — {detail}" if detail else ""))
    failed = sum(1 for s, _, _ in results if s == FAIL)
    print()
    if failed:
        print(f"  {failed} line(s) failing. The message above each one is the "
              f"whole hint you get.")
        print("  Ask what a line does. Do not ask for the file.")
    else:
        print("  Week 01 complete. Now answer the three questions in README.md "
              "out loud, without looking.")
    return failed


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
