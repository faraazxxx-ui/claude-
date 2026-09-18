#!/usr/bin/env python3
"""
PreToolUse gate for the Python literacy track.

The rule, from week-01-read-your-own-code/README.md:

    You may ask an AI to explain any line. You may not ask it to rewrite
    the file.

As prose in a README that is a request. Here it is a refusal. Reading,
running and explaining the protected files stays allowed; writing to them
does not.

Protected, in every week-* directory:
    specimen.py   the file you are learning to read
    check.py      the verifier — if a model can rewrite the grader,
                  the grade means nothing

A Bash command is judged clause by clause: the mutating verb and the
protected path have to occur in the SAME clause. Without that, a compound
command that merely reads the specimen and separately cleans a build
directory gets blocked for no reason.

Fails OPEN on unparseable input. This is a learning guardrail, not a
security boundary, and a gate that blocks every tool call when it cannot
read its own stdin is worse than no gate.
"""

import json
import re
import sys

PROTECTED = re.compile(r"week-[^/\s'\"]*/(specimen|check)\.py\b")

# Splits a shell command into clauses. A mutator only counts against a
# protected path if both land in the same clause.
CLAUSE_SPLIT = re.compile(r"(?:&&|\|\||[;\n|])")

# Constructs that mutate a file.
MUTATORS = [
    r">>?\s*\S*week-[^/\s'\"]*/(specimen|check)\.py",   # redirect into it
    r"\bsed\b[^;]*-[A-Za-z]*i",                         # sed -i / -i.bak
    r"\b(tee|dd|truncate|shred|install|patch)\b",
    r"\b(cp|mv|rsync|ln)\b",
    r"\b(rm|unlink)\b",
    r"\bgit\s+(checkout|restore|stash|reset|apply|clean)\b",
    r"open\s*\([^)]*['\"][wax]",                        # python inline write
    r"\.(write_text|writelines|write)\s*\(",
]

WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")

RULE = (
    "The rule in week-01-read-your-own-code/README.md: an AI may explain "
    "any line of this file, but may not rewrite it."
)


def deny(reason):
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # fail open — see module docstring

    tool = data.get("tool_name") or ""
    args = data.get("tool_input") or {}
    if not isinstance(args, dict):
        sys.exit(0)

    if tool in WRITE_TOOLS:
        path = str(
            args.get("file_path") or args.get("notebook_path") or ""
        ).replace("\\", "/")
        if PROTECTED.search(path):
            deny(
                f"Blocked: {tool} on a protected training file.\n{RULE}\n"
                "Reading it, running it and explaining any line are all "
                "allowed. The edit is Dr. Rahman's to make."
            )

    elif tool == "Bash":
        cmd = str(args.get("command") or "")
        for clause in CLAUSE_SPLIT.split(cmd):
            if PROTECTED.search(clause) and any(
                re.search(p, clause) for p in MUTATORS
            ):
                deny(
                    "Blocked: this command would modify a protected "
                    f"training file.\n{RULE}\n"
                    "`python3 specimen.py`, `python3 check.py`, `cat` and "
                    "`grep` are all still fine."
                )

    sys.exit(0)


if __name__ == "__main__":
    main()
