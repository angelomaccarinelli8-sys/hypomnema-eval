import argparse
import json
from pathlib import Path
import random
import yaml
import pandas as pd
from tqdm import tqdm

from eval.adapters import get_adapter
from eval.metrics import exact_match, f1_token, faithfulness_heuristic


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_toy_dataset() -> list[dict]:
    dataset_path = Path("eval/datasets/toy_suite.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(samples: list[dict], adapter, config: dict) -> pd.DataFrame:
    rows = []
    for sample in tqdm(samples, desc="Evaluating"):
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

    return pd.DataFrame(rows)


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
    df = evaluate(samples, adapter, config)

    run_name = config.get("run", {}).get("run_name", "run")
    output_dir = Path(config.get("run", {}).get("output_dir", "eval/results"))
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_path = output_dir / f"raw_{run_name}.jsonl"
    with open(raw_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")

    metrics = {
        "run_name": run_name,
        "mode": config.get("run", {}).get("mode", "unknown"),
        "suite": config.get("run", {}).get("suite", "unknown"),
        "n": len(df),
        "exact_match": float(df["exact_match"].mean()),
        "f1": float(df["f1"].mean()),
        "faithfulness": float(df["faithfulness"].mean()),
    }

    metrics_path = output_dir / f"metrics_{run_name}.csv"
    pd.DataFrame([metrics]).to_csv(metrics_path, index=False)

    print(f"Saved raw outputs to: {raw_path}")
    print(f"Saved metrics to: {metrics_path}")


if __name__ == "__main__":
    main()
