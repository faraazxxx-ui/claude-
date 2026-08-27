# Learnings

- 2026-08-27 · Uploads of the same handwritten page can arrive as byte-different PDFs (re-export); checksum before assuming duplicates, render before assuming difference.
- 2026-08-27 · Gmail connector identity is cheap to verify: one `in:sent` metadata query exposes the account address. Do this before promising email coverage.
