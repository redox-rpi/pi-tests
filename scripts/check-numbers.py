#!/usr/bin/env python3
"""Check pi-tests row numbers in queue.md.

Fails when a test number is used twice (queue table and Done table
together), or when the "Next number" line is not higher than every number
used in queue.md and reports/. A Done line or a queue row may repeat a
number when it is a step, part or rerun of that test (the word follows
the number in a Done line, or starts the Test cell of a queue row). Clashes
below BASELINE are older than this check and only warned about. Warns
when an open queue row already has a report file.
"""
import re, sys, pathlib

BASELINE = 600
root = pathlib.Path(__file__).resolve().parent.parent
text = (root / "queue.md").read_text()

section, rows = None, []
for line in text.splitlines():
    if line.startswith("## "):
        section = line[3:].strip()
        continue
    if section == "Queue":
        m = re.match(r"\|\s*(\d+)\s*\|", line)
        if m:
            again = re.match(r"\|\s*\d+\s*\|\W*(step|part|rerun)\b", line, re.I)
            rows.append(("queue-again" if again else "queue", int(m.group(1))))
    elif section == "Done":
        m = re.match(r"\|[^|]*\|\s*(\d+)\b", line)
        if m:
            again = re.match(r"\|[^|]*\|\s*\d+\s*(\(\w+\)\s*)?(step|part|rerun)", line, re.I)
            rows.append(("done-again" if again else "done", int(m.group(1))))

errors, warnings = [], []
seen = {}
for where, n in rows:
    if where in ("done-again", "queue-again"):
        continue
    if n in seen and not (seen[n] == "queue" and where == "done"):
        (errors if n >= BASELINE else warnings).append(
            f"test {n} is used twice ({seen[n]} and {where})")
    elif n in seen and seen[n] == "queue":
        (errors if n >= BASELINE else warnings).append(
            f"test {n} is open in the queue and also done")
    seen.setdefault(n, where)

reports = {int(p.stem) for p in (root / "reports").glob("*.md") if p.stem.isdigit()}
for where, n in rows:
    if where == "queue" and n in reports:
        warnings.append(f"open test {n} already has reports/{n}.md")

m = re.search(r"\*\*Next number:\s*(\d+)\*\*", text)
highest = max([n for _, n in rows] + list(reports) + [0])
if not m:
    errors.append('no "**Next number: N**" line in queue.md')
elif int(m.group(1)) <= highest:
    errors.append(f"Next number {m.group(1)} is not above the highest used number {highest}")

for w in warnings:
    print("warning:", w)
for e in errors:
    print("error:", e)
print(f"{len(rows)} rows, highest number {highest}")
sys.exit(1 if errors else 0)
