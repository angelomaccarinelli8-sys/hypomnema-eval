import argparse
import csv
from pathlib import Path


METRIC_COLUMNS = ["exact_match", "f1", "faithfulness"]


def read_metrics(metrics_dir: Path):
    rows = []
    for p in sorted(metrics_dir.glob("metrics_*.csv")):
        with open(p, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="eval/results")
    parser.add_argument("--out", default="eval/reports/summary.md")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = read_metrics(results_dir)
    if not rows:
        raise FileNotFoundError(f"No metrics_*.csv found in {results_dir}")

    lines = []
    lines.append("# Evaluation Summary\n")
    lines.append("## Runs\n")
    lines.append("| run_name | mode | suite | n | exact_match | f1 | faithfulness |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r['run_name']} | {r['mode']} | {r['suite']} | {r['n']} | {float(r['exact_match']):.4f} | {float(r['f1']):.4f} | {float(r['faithfulness']):.4f} |"
        )
    lines.append("\n")

    baseline = [r for r in rows if r["mode"] == "baseline"]
    memory_on = [r for r in rows if r["mode"] == "memory_on"]

    if baseline and memory_on:
        b = baseline[-1]
        m = memory_on[-1]
        lines.append("## Delta (latest baseline vs latest memory_on)\n")
        lines.append("| metric | baseline | memory_on | delta |")
        lines.append("|---|---:|---:|---:|")
        for col in METRIC_COLUMNS:
            b_val = float(b[col])
            m_val = float(m[col])
            delta = m_val - b_val
            lines.append(f"| {col} | {b_val:.4f} | {m_val:.4f} | {delta:+.4f} |")
        lines.append("\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary written to: {out_path}")


if __name__ == "__main__":
    main()
