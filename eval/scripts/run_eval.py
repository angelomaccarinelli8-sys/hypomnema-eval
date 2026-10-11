import argparse
import json
import random
from pathlib import Path

import yaml

from eval.adapters import get_adapter
from eval.metrics import exact_match, f1_token, faithfulness_heuristic


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_toy_dataset() -> list[dict]:
    dataset_path = Path("eval/datasets/toy_suite.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(samples: list[dict], adapter, config: dict) -> list[dict]:
    rows = []
    for sample in samples:
        pred = adapter.answer(sample, config)
        ref = sample["answer"]
        ctx = sample.get("context", "")

        rows.append(
            {
                "id": sample["id"],
                "type": sample.get("type", "unknown"),
                "prediction": pred,
                "reference": ref,
                "exact_match": exact_match(pred, ref),
                "f1": f1_token(pred, ref),
                "faithfulness": faithfulness_heuristic(pred, ctx),
            }
        )
    return rows


def write_metrics_csv(run_name: str, mode: str, suite: str, rows: list[dict], output_dir: Path):
    total = len(rows)
    if total == 0:
        exact = 0.0
        f1 = 0.0
        faith = 0.0
    else:
        exact = sum(r["exact_match"] for r in rows) / total
        f1 = sum(r["f1"] for r in rows) / total
        faith = sum(r["faithfulness"] for r in rows) / total

    metrics = {
        "run_name": run_name,
        "mode": mode,
        "suite": suite,
        "n": total,
        "exact_match": exact,
        "f1": f1,
        "faithfulness": faith,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / f"metrics_{run_name}.csv"
    with open(metrics_path, "w", encoding="utf-8") as f:
        fields = ["run_name", "mode", "suite", "n", "exact_match", "f1", "faithfulness"]
        f.write(",".join(fields) + "\n")
        f.write(",".join(str(metrics.get(field, "")) for field in fields) + "\n")
    return metrics_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--suite", default="toy")
    args = parser.parse_args()

    config = load_config(args.config)
    seed = config.get("run", {}).get("seed", 42)
    random.seed(seed)

    adapter_type = config.get("adapter", {}).get("adapter_type", "echo")
    adapter = get_adapter(adapter_type)

    if args.suite != "toy":
        raise ValueError("Only suite=toy is currently wired. Extend run_eval.py for additional public datasets.")

    samples = load_toy_dataset()
    rows = evaluate(samples, adapter, config)

    run_name = config.get("run", {}).get("run_name", "run")
    mode = config.get("run", {}).get("mode", "unknown")
    suite = config.get("run", {}).get("suite", "unknown")
    output_dir = Path(config.get("run", {}).get("output_dir", "eval/results"))

    raw_path = output_dir / f"raw_{run_name}.jsonl"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(raw_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    metrics_path = write_metrics_csv(run_name, mode, suite, rows, output_dir)
    print(f"Saved raw outputs to: {raw_path}")
    print(f"Saved metrics to: {metrics_path}")


if __name__ == "__main__":
    main()
