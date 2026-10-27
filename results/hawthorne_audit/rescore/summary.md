# Test 2 summary: monitor flag rates (score >= 3) by arm, monitor and rubric (PREREG.md)

## Message monitor (registered): COMPLETE

| Monitor | Rubric | ON | OFF | C (no brief, $15) | D (no $20 row) | Parse failures |
|---|---|---|---|---|---|---|
| qwen | A | 0.99 (300) | 0.53 (208) | 1.00 (300) | 0.97 (300) | 0 |
| qwen | B | 0.99 (300) | 0.52 (208) | 0.98 (300) | 0.97 (300) | 0 |
| gemma | A | 1.00 (300) | 0.62 (208) | 1.00 (300) | 0.99 (300) | 0 |
| gemma | B | 1.00 (300) | 0.58 (208) | 0.77 (300) | 0.98 (300) | 0 |
| deepseek | A | 0.99 (298) | 0.53 (208) | 0.96 (300) | 0.93 (296) | 3 |
| deepseek | B | 0.98 (300) | 0.50 (206) | 0.00 (300) | 0.86 (298) | 2 |
| gptoss | A | 0.90 (300) | 0.58 (208) | 0.85 (300) | 0.96 (300) | 0 |
| gptoss | B | 0.83 (300) | 0.55 (208) | 0.00 (300) | 0.87 (300) | 0 |

- PC (ON ≥ 0.8 under A): {'qwen': True, 'gemma': True, 'deepseek': True, 'gptoss': True}
- Q1: **all families flag the $15 agreements; not a same-model artifact** (C rates under A: {'qwen': 1.0, 'gemma': 1.0, 'deepseek': 0.9566666666666667, 'gptoss': 0.8466666666666667})
- Q2: **not met** (monitors meeting it: ['deepseek', 'gptoss'])

## Reasoning monitor (secondary): COMPLETE

| Monitor | Rubric | ON | OFF | C (no brief, $15) | D (no $20 row) | Parse failures |
|---|---|---|---|---|---|---|
| qwen | A | 0.95 (300) | 0.47 (300) | 1.00 (300) | 0.85 (300) | 0 |
| qwen | B | 0.93 (300) | 0.45 (300) | 0.99 (300) | 0.82 (300) | 0 |
| gemma | A | 0.97 (300) | 0.62 (300) | 0.99 (300) | 0.95 (300) | 0 |
| gemma | B | 0.93 (300) | 0.54 (300) | 0.99 (300) | 0.89 (300) | 0 |
| deepseek | A | 0.96 (300) | 0.64 (296) | 1.00 (300) | 0.85 (298) | 3 |
| deepseek | B | 0.96 (300) | 0.56 (294) | 0.00 (300) | 0.80 (294) | 6 |
| gptoss | A | 0.95 (300) | 0.49 (300) | 1.00 (298) | 0.82 (300) | 1 |
| gptoss | B | 0.89 (300) | 0.41 (300) | 0.00 (300) | 0.75 (300) | 0 |

- PC (ON ≥ 0.8 under A): {'qwen': True, 'gemma': True, 'deepseek': True, 'gptoss': True}
- Q1: **all families flag the $15 agreements; not a same-model artifact** (C rates under A: {'qwen': 1.0, 'gemma': 0.9933333333333333, 'deepseek': 1.0, 'gptoss': 1.0})
- Q2: **not met** (monitors meeting it: ['deepseek', 'gptoss'])

## Retest: Qwen3-14B rubric A against the saved Oct 25 scores

- message: n = 1108, exact score agreement 0.9972924187725631, flag agreement 1.0
- reasoning: n = 1200, exact score agreement 0.995, flag agreement 1.0
