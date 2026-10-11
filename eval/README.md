# Evaluation Protocol (v1)

This protocol is intentionally simple and reproducible.

## Objective

Measure whether enabling memory improves task performance compared to baseline:
- retrieval quality
- conversational memory correctness
- attribution/faithfulness behavior

## Experimental Conditions

- **A (baseline)**: memory disabled / not used
- **B (memory_on)**: memory enabled using normal pipeline

Only memory behavior should differ between A and B.

## Reproducibility Requirements

Always record:
- repository + commit hash under test
- model name/version
- decoding params (temperature, max tokens)
- seeds (if applicable)
- dataset names + split
- run date/time

## Metrics

Current minimal metrics in this repo:
- `exact_match`
- `f1`
- `faithfulness` (heuristic placeholder)

You should add benchmark-specific metrics as you integrate public datasets.

## Reporting

For each suite/dataset, report:
- baseline score
- memory_on score
- absolute delta
- relative delta (%)

Also include 5-10 failure examples.
