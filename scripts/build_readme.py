import json
from pathlib import Path
import sys

DATA = Path(__file__).resolve().parents[1] / "data" / "benchmarks.json"

if not DATA.exists():
    print("ERROR: benchmarks.json not found at", DATA, file=sys.stderr)
    sys.exit(1)

try:
    items = json.loads(DATA.read_text())
except Exception as e:
    print("ERROR: Failed to parse benchmarks.json:", e, file=sys.stderr)
    sys.exit(1)

if not items:
    print("WARNING: benchmarks.json is empty — no benchmarks to render.", file=sys.stderr)
    sys.exit(0)

TEMPLATE = "- **{name}** ({year}) — {tasks}; langs: {langs}{runner}\n  {links}\n"

def fmt_links(item):
    parts = []
    for k in ("paper", "code", "dataset"):
        if url := item.get(k):
            parts.append(f"[{k}]({url})")
    return " · ".join(parts)

lines = []
for it in sorted(items, key=lambda x: x["name"].lower()):
    tasks = ", ".join(it.get("tasks", [])) or "—"
    langs = ", ".join(it.get("langs", [])) or "—"
    runner = f"; runner: {it['runner']}" if it.get("runner") else ""
    links = fmt_links(it)
    lines.append(TEMPLATE.format(
        name=it['name'], year=it['year'], tasks=tasks,
        langs=langs, runner=runner, links=links
    ))

print("\n".join(lines))

