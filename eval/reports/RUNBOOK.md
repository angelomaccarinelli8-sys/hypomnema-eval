# Runbook

## Standard flow

1. Configure baseline and memory-on YAML files in `eval/configs/`.
2. Run baseline:

```bash
python -m eval.scripts.run_eval --config eval/configs/baseline.yaml --suite toy
```

3. Run memory_on:

```bash
python -m eval.scripts.run_eval --config eval/configs/memory_on.yaml --suite toy
```

4. Aggregate:

```bash
python -m eval.scripts.aggregate_results --results-dir eval/results --out eval/reports/summary.md
```

## What to commit after each run

- `eval/results/metrics_*.csv`
- optionally `eval/results/raw_*.jsonl`
- updated report in `eval/reports/`
