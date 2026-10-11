import argparse
from pathlib import Path
import pandas as pd


METRIC_COLUMNS = ["exact_match", "f1", "faithfulness"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="eval/results")
    parser.add_argument("--out", default="eval/reports/summary.md")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    metric_files = sorted(results_dir.glob("metrics_*.csv"))
    if not metric_files:
        raise FileNotFoundError(f"No metrics_*.csv found in {results_dir}")

    frames = [pd.read_csv(p) for p in metric_files]
    df = pd.concat(frames, ignore_index=True)

    lines = []
    lines.append("# Evaluation Summary\n")
    lines.append("## Runs\n")
    try:
        lines.append(df.to_markdown(index=False))
    except Exception:
        lines.append(df.to_string(index=False))
    lines.append("\n")

    baseline = df[df["mode"] == "baseline"]
    memory_on = df[df["mode"] == "memory_on"]

    if not baseline.empty and not memory_on.empty:
        b = baseline.iloc[-1]
        m = memory_on.iloc[-1]
        lines.append("## Delta (latest baseline vs latest memory_on)\n")
        lines.append("| metric | baseline | memory_on | delta |")
        lines.append("|---|---:|---:|---:|")
        for col in METRIC_COLUMNS:
            if col in b and col in m:
                b_val = float(b[col])
                m_val = float(m[col])
                delta = m_val - b_val
                lines.append(f"| {col} | {b_val:.4f} | {m_val:.4f} | {delta:+.4f} |")
        lines.append("\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary written to: {out_path}")


if __name__ == "__main__":
    main()
