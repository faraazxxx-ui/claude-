# specimen.py — annotated read

Read this **after** you've tried each sitting yourself, not before. It explains what every line does. It does not tell you what to change.

The file has four blocks. Almost every Python script you own has these same four blocks in this same order, so learning the shape once transfers to all 4,793 lines in this repo.

| Lines | Block | Job |
|---|---|---|
| 1–11 | Setup | Announce dependencies, declare where things live |
| 13–34 | A worker function | Turn one CSV into one table |
| 36–55 | A second worker function | Same job, different file |
| 57–73 | The conductor | Call the workers in order, assemble, write out |

---

## Lines 1–11 · Setup

```python
#!/usr/bin/env python
import pandas as pd
import os
```

**Line 1** is not code. It's an instruction to the operating system for when a file is run directly: "use whatever `python` is on this machine." Your shell reads it; Python ignores it.

**Line 2** loads `pandas` — the library that gives Python a spreadsheet. Everything in your health scripts that resembles a table, a column, a merge, or a rolling average comes from here. `as pd` is a local nickname so the rest of the file can say `pd` instead of `pandas`. It's convention, not requirement. Every pandas script on earth says `pd`.

**Line 3** loads `os` — the standard library for talking to the filesystem: joining paths, making directories, checking what exists.

Think of these two lines as the formulary. Nothing in the script can use a drug that wasn't stocked at the top.

```python
UPLOAD_DIR = "/home/ubuntu/upload"
OUTPUT_DIR = "/home/ubuntu/work"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "processed_health_report.md")
```

**Lines 6–8** declare three constants. `ALL_CAPS` is a convention meaning *this is a setting, not a working value — change it here, not in twelve places below.* Whoever generated this file did that correctly.

`os.path.join` glues path pieces with the right separator for the operating system. On your Mac it produces a forward slash; on Windows a backslash. Writing `OUTPUT_DIR + "/processed_health_report.md"` would work today and break on a different machine. This is the careful version.

**The problem with lines 6 and 7 is not the technique — it's the addresses.** `/home/ubuntu/upload` was a temporary sandbox on a cloud machine that was destroyed when the session ended. The script is a prescription written to a pharmacy that has since closed.

```python
os.makedirs(OUTPUT_DIR, exist_ok=True)
```

**Line 11** creates the output directory. `exist_ok=True` means *don't complain if it's already there.*

This line is why Sitting 1 fails so quietly. It runs before anything else, at import time. It cheerfully created `/home/ubuntu/work/` on your machine — a directory that has no business existing — and gave the script somewhere to write its empty report. Without this line you'd have gotten an error and known immediately.

---

## Lines 13–34 · `process_physio_data`

```python
def process_physio_data():
    """Processes physiological_cycles.csv and returns a markdown table."""
```

`def` defines a function: a named procedure that does one thing and hands back a result. The `()` is empty, meaning it takes no inputs — it gets everything it needs from those constants above. That's a design weakness you'll meet again: the function can only ever read one specific file, because the filename is welded in at line 16 rather than passed in.

The line in triple quotes is a **docstring** — documentation that lives inside the code and can be read by tools. This one is accurate. Many in this repo are not; a docstring is a claim, not a guarantee.

```python
    try:
        df = pd.read_csv(os.path.join(UPLOAD_DIR, "physiological_cycles.csv"))
```

`try:` opens a protected block: *attempt this, and if a specific kind of failure occurs, jump to the handler instead of crashing.*

`pd.read_csv` reads the file into a **DataFrame** — pandas' table object, conventionally named `df`. It arrives with named columns and numbered rows, and from here on it behaves like a spreadsheet you can slice.

```python
        df_selected = df[[
            "Cycle start time",
            "Recovery score %",
            ...
        ]].copy()
```

**Lines 17–25** are column selection. The doubled brackets `[[...]]` are not a typo: the outer pair means *index into this table*, the inner pair is *a list of the columns I want*. Single brackets with one name give you one column; double brackets with a list give you a narrower table.

**This is the line that carries the script's hidden assumption.** Those seven strings are a contract with the input file. If the CSV doesn't have a column spelled *exactly* that way — capitalization, spacing, the `%` sign — pandas raises a `KeyError` and stops. Nobody wrote that contract down anywhere a human would find it. It lives here, implied.

`.copy()` matters more than it looks. Without it, `df_selected` would be a *view* into the original table, and editing it can throw a warning or silently change the parent. `.copy()` says: give me my own independent table. Generated code often omits this and produces intermittent, hard-to-trace bugs.

```python
        df_selected.columns = [
            "Date", "Recovery (%)", "RHR (bpm)", ...
        ]
```

**Lines 26–29** rename by positional replacement — the first new name replaces the first old name, and so on. It is fast and it is fragile: if someone adds a column to the selection list at line 17 and forgets to add a name here, the lists fall out of alignment and **every column silently gets the wrong label.** No error. Your HRV column would be labelled RHR and the report would look perfectly normal.

The safer form is `df.rename(columns={"old": "new"})`, which pairs names explicitly and can't drift. Worth knowing, because you'll see both across your repo.

```python
        df_selected["Date"] = pd.to_datetime(df_selected["Date"]).dt.date
        df_selected = df_selected.sort_values(by="Date", ascending=False)
        return df_selected.to_markdown(index=False)
```

**Line 30** converts text into real dates. A CSV has no types — everything arrives as a string. `"2024-04-05"` is characters until `pd.to_datetime` makes it a date. `.dt.date` then strips the time portion, keeping just the calendar day. Without this, sorting would be alphabetical, which happens to work for `YYYY-MM-DD` and breaks for every other format.

**Line 31** sorts newest first. **Line 32** renders the table as markdown text and hands it back. `index=False` drops pandas' automatic row numbers, which are meaningless here. `to_markdown` needs the `tabulate` library — which is why `setup.sh` installs it even though the script never imports it by name. An invisible dependency.

```python
    except FileNotFoundError:
        return "_Physiological data file not found._"
```

**Lines 33–34 are the most important lines in the file, and they are the ones doing the damage.**

This catches the specific failure "that file isn't there" and, instead of stopping, returns an italic sentence that gets pasted into the report as if it were content. The function's contract is *return a markdown table*; this returns a markdown apology. Both are strings, so nothing downstream can tell the difference.

The intent was kindness: don't let one missing file kill the whole run. The effect is a clinical report that looks finished and contains nothing — and reports success while doing it.

There is a defensible version of this pattern. It looks like: catch the error, write a warning to the error stream, and **exit non-zero** so that anything automated downstream knows the run was incomplete. This version does none of that.

---

## Lines 36–55 · `process_sleep_data`

Structurally identical to the first function — same try, same selection, same rename, same return. Two things differ.

```python
        df_selected["Sleep Onset"] = pd.to_datetime(df_selected["Sleep Onset"]).dt.strftime("%H:%M")
```

**Lines 50–51** convert full timestamps into clock strings: `2024-04-06 00:48:45` becomes `00:48`. `strftime` is "string format time"; `%H:%M` is 24-hour hours and minutes.

Note what this throws away. After this line, sleep onset is **text, not time**. You can print it; you cannot subtract it, average it, or compute a standard deviation from it. Your own health-analyst skill states that your sleep-onset SD of ~5.75 hours is equivalent to chronic shift work — that number cannot be computed from this script's output, because this line destroyed the ability to compute it. Formatting for display and keeping data usable are different goals, and this line quietly chose the first.

The second difference is line 44, which asks for `In bed duration (min)` — a column your cleaned data does not contain in any form. That's Sitting 3.

---

## Lines 57–73 · `main` and the guard

```python
def main():
    physio_table = process_physio_data()
    sleep_table = process_sleep_data()
```

The conductor. Calls each worker, holds each result in a named variable. Both are now strings — either a real table or an apology, and `main` has no way to tell which. **That's the architectural flaw**, not a typo: the functions' return type doesn't distinguish success from failure, so the caller can't check.

```python
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Processed Health Data Report\n\n")
        ...
```

`with open(...) as f:` opens the file and guarantees it gets closed afterwards, even if something fails partway. `"w"` means write — **it truncates the file to empty first.** Every run destroys the previous report. There's no versioning and no warning.

The `\n` are newlines. `f.write` appends text in sequence; the blank lines matter because markdown needs them between blocks.

Notice line 64: the report asserts it "consolidates the latest raw data into a clean, analyzable format." That sentence is hardcoded. It prints whether or not any data was read. **The document's claim about itself is independent of what the document contains.**

```python
    print(f"Processed health report generated at: {OUTPUT_FILE}")
```

**Line 70.** The `f` before the quote makes it an *f-string*: anything in `{braces}` gets substituted with that variable's value. This prints unconditionally, after a write that may have written nothing. This is the line that told you "success" in Sitting 1.

```python
if __name__ == "__main__":
    main()
```

**Lines 72–73.** The standard Python idiom for *only do this when the file is run directly, not when it's imported by another file.* `__name__` is set to `"__main__"` when you run `python specimen.py`, and to the module's name when something imports it.

This is why `check.py` can import this file, read its settings, and call `main()` deliberately — without the script auto-running on import. It's a small thing that makes code reusable rather than only executable.

---

## The summary you should carry to Week 2

Five patterns here recur in every script in this repo:

1. **Constants at the top** are the settings. When a script won't run, look there first.
2. **Column selection is an undocumented contract** with the input file's shape.
3. **A bare `except` that returns a normal-looking value** converts a loud failure into a silent one. Hunt these.
4. **Formatting for display can destroy analysability.** Ask what a transformation throws away.
5. **A script's claims about itself are just text.** They print whether or not they're true.

You now know enough to read `deadline_tracker.py`. It has no pandas at all — just dates, conditionals, and the same four-block shape.
