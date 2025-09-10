import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "data" / "schema.json").read_text())
DATA = json.loads((ROOT / "data" / "benchmarks.json").read_text())

errors = []
validator = Draft202012Validator(SCHEMA)
for idx, item in enumerate(DATA):
    for err in validator.iter_errors(item):
        errors.append(f"Item {idx} ({item.get('name','<no-name>')}): {err.message}")

if errors:
    print("Schema validation failed:\n" + "\n".join(errors))
    raise SystemExit(1)
else:
    print("✔ Schema validation passed for", len(DATA), "items.")

