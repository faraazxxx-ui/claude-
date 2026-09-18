#!/usr/bin/env python3
"""Test the protect-specimen PreToolUse gate. Run: python3 test_gate.py

Test data lives in this file rather than in a shell command on purpose --
the gate inspects Bash command text, so a shell-based test harness trips
its own assertions.
"""
import json
import subprocess
import sys

HOOK = "/home/user/claude-/.claude/hooks/protect-specimen.py"
W = "week-01-read-your-own-code"

CASES = [
    # (expect, name, payload)
    ("DENY", "Write specimen.py", {"tool_name": "Write", "tool_input": {"file_path": f"{W}/specimen.py"}}),
    ("DENY", "Edit specimen.py (abs path)", {"tool_name": "Edit", "tool_input": {"file_path": f"/home/user/claude-/{W}/specimen.py"}}),
    ("DENY", "MultiEdit specimen.py", {"tool_name": "MultiEdit", "tool_input": {"file_path": f"{W}/specimen.py"}}),
    ("DENY", "Write check.py (the grader)", {"tool_name": "Write", "tool_input": {"file_path": f"{W}/check.py"}}),
    ("DENY", "future week-02 specimen", {"tool_name": "Write", "tool_input": {"file_path": "week-02-deadlines/specimen.py"}}),
    ("DENY", "sed -i on specimen", {"tool_name": "Bash", "tool_input": {"command": f"sed -i 's/a/b/' {W}/specimen.py"}}),
    ("DENY", "sed -i.bak on specimen", {"tool_name": "Bash", "tool_input": {"command": f"sed -i.bak 's/a/b/' {W}/specimen.py"}}),
    ("DENY", "heredoc redirect onto specimen", {"tool_name": "Bash", "tool_input": {"command": f"cat > {W}/specimen.py <<EOF\nx\nEOF"}}),
    ("DENY", "append redirect onto specimen", {"tool_name": "Bash", "tool_input": {"command": f"echo x >> {W}/specimen.py"}}),
    ("DENY", "cp fixed file onto specimen", {"tool_name": "Bash", "tool_input": {"command": f"cp fixed.py {W}/specimen.py"}}),
    ("DENY", "mv onto specimen", {"tool_name": "Bash", "tool_input": {"command": f"mv tmp.py {W}/specimen.py"}}),
    ("DENY", "git checkout revert specimen", {"tool_name": "Bash", "tool_input": {"command": f"git checkout -- {W}/specimen.py"}}),
    ("DENY", "rm specimen", {"tool_name": "Bash", "tool_input": {"command": f"rm {W}/specimen.py"}}),
    ("DENY", "tee onto specimen", {"tool_name": "Bash", "tool_input": {"command": f"echo x | tee {W}/specimen.py"}}),
    ("DENY", "python inline open(...,'w')", {"tool_name": "Bash", "tool_input": {"command": f"python3 -c \"open('{W}/specimen.py','w').write('')\""}}),

    ("ALLOW", "run specimen.py", {"tool_name": "Bash", "tool_input": {"command": f"python3 {W}/specimen.py"}}),
    ("ALLOW", "run check.py", {"tool_name": "Bash", "tool_input": {"command": f"cd {W} && python3 check.py"}}),
    ("ALLOW", "cat specimen.py", {"tool_name": "Bash", "tool_input": {"command": f"cat -n {W}/specimen.py"}}),
    ("ALLOW", "grep specimen.py", {"tool_name": "Bash", "tool_input": {"command": f"grep -n import {W}/specimen.py"}}),
    ("ALLOW", "diff specimen against source", {"tool_name": "Bash", "tool_input": {"command": f"diff {W}/specimen.py skill/scripts/process_health_data.py"}}),
    ("ALLOW", "Read specimen.py", {"tool_name": "Read", "tool_input": {"file_path": f"{W}/specimen.py"}}),
    ("ALLOW", "Write README.md", {"tool_name": "Write", "tool_input": {"file_path": f"{W}/README.md"}}),
    ("ALLOW", "Write ANNOTATED.md", {"tool_name": "Write", "tool_input": {"file_path": f"{W}/ANNOTATED.md"}}),
    ("ALLOW", "Write setup.sh", {"tool_name": "Bash", "tool_input": {"command": f"chmod +x {W}/setup.sh"}}),
    ("ALLOW", "unrelated rm", {"tool_name": "Bash", "tool_input": {"command": "rm -rf out/"}}),
    # the over-block this revision fixes: read specimen in one clause,
    # unrelated cleanup in another
    ("ALLOW", "read specimen && unrelated rm", {"tool_name": "Bash", "tool_input": {"command": f"cat {W}/specimen.py && rm -rf out/"}}),
    ("ALLOW", "run specimen ; unrelated cp", {"tool_name": "Bash", "tool_input": {"command": f"python3 {W}/specimen.py ; cp a.txt b.txt"}}),
]


def run(payload):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True)
    return "DENY" if p.returncode == 2 else "ALLOW"


def main():
    failed = 0
    for expect, name, payload in CASES:
        got = run(payload)
        ok = got == expect
        if not ok:
            failed += 1
        print(f"  {'ok  ' if ok else 'FAIL'}  {got:<5} (want {expect:<5})  {name}")

    # fail-open on garbage input
    p = subprocess.run([sys.executable, HOOK], input="not json",
                       capture_output=True, text=True)
    ok = p.returncode == 0
    failed += 0 if ok else 1
    print(f"  {'ok  ' if ok else 'FAIL'}  {'ALLOW' if ok else 'DENY':<5} "
          f"(want ALLOW)  malformed stdin fails open")

    print(f"\n  {len(CASES) + 1 - failed}/{len(CASES) + 1} passing"
          + ("" if not failed else f" — {failed} FAILING"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
