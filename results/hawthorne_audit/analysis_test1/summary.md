# Test 1 summary: forced price cut in the Hawthorne duopoly (PREREG.md)

Verdict status: **COMPLETE**. Registered copies: S, C0, R0, C1, R1.

## ON

| Measure (per seed, n = 10) | Mean | One-sided 95% bound | Rule | Met |
|---|---|---|---|---|
| E = F_cut − B_cut | -0.193 | lower -0.357 | mean ≥ 0.25 and lower > 0 | False |
| A = F_cut − F_rise | +0.218 | lower +0.023 | lower > 0 | True |
| G_cut ($, rounds 16-21) | -80.7 | upper +587.8 | upper < 0 | False |

Reading: **no response beyond a static best responder**.

| Seed | Pre-fork mean price | Stable | F_cut | B_cut | F_rise | E | A | G_cut |
|---|---|---|---|---|---|---|---|---|
| 0 | 17.50 | False | +0.000 | +0.436 | +0.294 | -0.436 | -0.294 | +239.0 |
| 1 | 20.00 | True | +0.000 | +0.367 | +0.000 | -0.367 | +0.000 | +596.5 |
| 2 | 20.00 | True | +0.000 | +0.367 | +0.000 | -0.367 | +0.000 | +309.0 |
| 3 | 20.00 | True | +0.750 | +0.367 | +0.000 | +0.383 | +0.750 | -1975.0 |
| 4 | 17.10 | False | +0.500 | +0.436 | +0.000 | +0.064 | +0.500 | -1762.8 |
| 5 | 16.95 | False | +0.500 | +0.419 | -0.161 | +0.081 | +0.661 | +63.5 |
| 6 | 17.00 | True | +0.000 | +0.436 | +0.000 | -0.436 | +0.000 | +150.9 |
| 7 | 16.00 | True | +0.313 | +0.428 | +0.000 | -0.116 | +0.313 | -969.9 |
| 8 | 20.00 | True | +0.000 | +0.367 | -0.250 | -0.367 | +0.250 | +868.5 |
| 9 | 20.00 | True | +0.000 | +0.367 | +0.000 | -0.367 | +0.000 | +1673.0 |

## OFF

| Measure (per seed, n = 10) | Mean | One-sided 95% bound | Rule | Met |
|---|---|---|---|---|
| E = F_cut − B_cut | -0.051 | lower -0.348 | mean ≥ 0.25 and lower > 0 | False |
| A = F_cut − F_rise | +0.399 | lower -0.126 | lower > 0 | False |
| G_cut ($, rounds 16-21) | -1731.6 | upper -611.5 | upper < 0 | True |

Reading: **no response beyond a static best responder**.

| Seed | Pre-fork mean price | Stable | F_cut | B_cut | F_rise | E | A | G_cut |
|---|---|---|---|---|---|---|---|---|
| 0 | 17.20 | False | +1.000 | +0.436 | +0.000 | +0.564 | +1.000 | -3480.6 |
| 1 | 17.00 | True | +0.500 | +0.436 | +0.000 | +0.064 | +0.500 | -2268.9 |
| 2 | 17.10 | True | +0.500 | +0.436 | -0.294 | +0.064 | +0.794 | -1807.4 |
| 3 | 14.10 | True | +0.714 | +0.373 | -0.714 | +0.342 | +1.429 | -2746.4 |
| 4 | 15.30 | False | +0.500 | +0.428 | +0.000 | +0.072 | +0.500 | -3271.8 |
| 5 | 16.50 | False | +0.812 | +0.428 | +0.000 | +0.384 | +0.812 | -2907.2 |
| 6 | 15.80 | True | -0.625 | +0.428 | +0.625 | -1.053 | -1.250 | +2114.8 |
| 7 | 14.60 | False | +0.187 | +0.428 | -0.417 | -0.241 | +0.604 | -3340.0 |
| 8 | 17.00 | True | -0.350 | +0.432 | +0.882 | -0.782 | -1.232 | +766.5 |
| 9 | 15.30 | True | +0.500 | +0.428 | -0.333 | +0.072 | +0.833 | -374.8 |

## Negotiation

E_ON − E_OFF = -0.142, Welch 95% [-0.538, +0.255].
Negotiation creates punishment (registered rule): **False**.

