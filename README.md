# hypomnema-eval

Public evaluation harness for **hypomnema** (and similar memory systems), focused on:
- retrieval effectiveness
- conversational memory consistency
- faithfulness/attribution quality

This repository is designed to be transparent and reproducible.

## Quickstart

1. Create a Python virtual environment
2. Install dependencies
3. Configure your adapter and run baseline + memory-on experiments
4. Generate report-ready summaries

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\\Scripts\\activate  # Windows PowerShell

pip install -r requirements.txt
```

### 2) Configure

Edit these files:
- `eval/configs/baseline.yaml`
- `eval/configs/memory_on.yaml`

Set at least:
- `adapter_type` (`hypomnema_jsonl` or `echo`)
- model parameters
- paths and run metadata

### 3) Run (toy suite)

```bash
python -m eval.scripts.run_eval --config eval/configs/baseline.yaml --suite toy
python -m eval.scripts.run_eval --config eval/configs/memory_on.yaml --suite toy
python -m eval.scripts.aggregate_results --results-dir eval/results --out eval/reports/summary.md
```

### 4) Outputs

- raw outputs: `eval/results/raw_*`
- metrics: `eval/results/metrics_*`
- report summary: `eval/reports/summary.md`

## Adapters

### `echo` adapter
Returns the reference answer from the sample. Useful only as smoke test for the pipeline.

### `hypomnema_jsonl` adapter
A minimal local adapter that reads memory entries from a JSONL file and retrieves by lexical overlap.

Expected config keys:

```yaml
adapter:
  adapter_type: hypomnema_jsonl
  memory_enabled: true
  memory_store_path: eval/datasets/hypomnema_memory.jsonl
```

Each JSONL line can include fields like:
- `text` (preferred), or
- `content` (fallback)

This is a practical baseline integration layer and can be replaced by your production adapter.

## Notes

- The included `toy` suite is intentionally small and local so the repo is usable immediately.
- Replace/add datasets in `eval/datasets/` and wire them in `eval/scripts/run_eval.py`.
- The adapter layer (`eval/adapters/base.py`) is where you connect your real system.
