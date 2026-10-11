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
- `adapter_type`
- model parameters
- paths and run metadata

### 3) Run

```bash
python -m eval.scripts.run_eval --config eval/configs/baseline.yaml --suite toy
python -m eval.scripts.run_eval --config eval/configs/memory_on.yaml --suite toy
python -m eval.scripts.aggregate_results --results-dir eval/results --out eval/reports/summary.md
```

### 4) Outputs

- raw outputs: `eval/results/raw_*`
- metrics: `eval/results/metrics_*`
- report summary: `eval/reports/summary.md`

## Notes

- The included `toy` suite is intentionally small and local so the repo is usable immediately.
- Replace/add datasets in `eval/datasets/` and wire them in `eval/scripts/run_eval.py`.
- The adapter layer (`eval/adapters/base.py`) is where you connect your real system.
