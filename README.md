# GRAFT++: Reducing Collusive Behavior in Agents via Localized Training and J-space Monitoring

**Alfredo Frontera, Jayden Jeong, Jake Li, Rohan Dash** · Columbia University (Columbia AI Alignment Club)
Apart Research, AI Collusion Research Sprint, October 23–25, 2026 (Track 3: collusion carriers and countermeasures)

This is the team's complete repository: the code, every run log, the pre-registrations, the results and the paper
sources, for both markets in the paper. The Hawthorne Market and GRAFT++ code is in [`graftpp/`](graftpp/),
imported unchanged from [github.com/xxozzi/graftpp](https://github.com/xxozzi/graftpp).

## The short version

Large language model agents now set prices, and they can collude by keeping prices high together. We asked what a
group of seller agents does when it learns it is being watched.

- **Cartels form, and we know what this one needs.** In the Hawthorne Market, sellers told only to maximize profit
  form cartels on their own. Without the payoff table in their prompt, none did. Without negotiation before each price,
  fewer did.
- **Watching changes the words more than the price.** Told that a monitor reads their channel, sellers lower their
  prices but keep making agreements. Sellers with nothing to gain from colluding go quiet too, so a quiet channel is not
  evidence that collusion stopped.
- **The same holds in a second market.** In a double auction, monitors cut coordinating messages but barely move
  prices, and a simple price check flags every cartel, while a message monitor misses about one in five.
- **The model's activations show what the messages hide.** A linear probe finds covert coordination better than a
  text monitor. GRAFT++ routes fine-tuning on that probe instead of the text monitor and removes more of the collusion
  the text monitor cannot see, though the gain falls short of the margin we pre-registered.

## Figures

![Two panels of bar charts for the double auction. Top row: the share of seller messages that coordinate, under no
monitor, a silent monitor, an announced monitor, fines with one, two or all sellers read, and sellers told to dodge.
The share falls under fines, most of all when every seller is read. Bottom row: the price index under the same
conditions, which stays almost the same everywhere. Left panel Qwen3-14B with three sellers, right panel GPT-4.1 with
five sellers.](graftpp/report/paper/figs/market2.png)

*Double auction: monitors and fines change what sellers say, not what they charge (paper Section 4.3).*

![Bar chart of the collusion index after fine-tuning, for the unwatched, watched and fined conditions. On the original
training set, naive fine-tuning and filtering keep high collusion while GRAFT, GRAFT on the reasoning judge and GRAFT++
remove it. On the text-blind training set, GRAFT colludes again while GRAFT++ stays lower.](graftpp/report/paper/figs/graft.png)

*Training collusion out: GRAFT++ against text-monitor GRAFT (paper Section 4.5).*

![Bar chart of the price index over rounds 16 to 30 in the Hawthorne duopoly, five games per arm. Full setup: mean
0.90. No same-round negotiation: 0.36. No brief: 0.06, every game at the competitive level. Brief without its 20 dollar
row: 0.47.](results/paper_figures/fig_hawthorne_intervention.png)

*What the Hawthorne cartel needs: the intervention test (paper Appendix B).*

## What is where

| Part of the paper | Where | Main author |
|---|---|---|
| Hawthorne Market, condition ladder, monitors, activation probes, GRAFT and GRAFT++ (Sections 3.1, 3.3, 3.4, 4.1, 4.2, 4.4, 4.5) | [`graftpp/`](graftpp/) (its own [README](graftpp/README.md)) | Jayden Jeong |
| Double auction: matched-history monitor conditions, fines, GPT-4.1 replication, price check, withholding variant (Sections 3.2, 4.3) | [`src/`](src/), [`scripts/`](scripts/), [`results/`](results/); every number mapped to its file in [`report/claims.md`](report/claims.md) | Alfredo Frontera |
| The intervention test in the Hawthorne duopoly (Appendix B) | [`results/hawthorne_negotiation/`](results/hawthorne_negotiation/) and [`results/hawthorne_negotiation_side_checks/`](results/hawthorne_negotiation_side_checks/) | Alfredo Frontera |
| Cartel formation without instruction in the double auction (Appendix C) | [`results/E5_runs.csv`](results/E5_runs.csv), [`results/NEWMARKET.md`](results/NEWMARKET.md), [`results/PRESSURE_V2.md`](results/PRESSURE_V2.md), [`results/DUO.md`](results/DUO.md), [`results/_launch_logs/`](results/_launch_logs/) | Alfredo Frontera |
| Paper figures | [`results/paper_figures/`](results/paper_figures/), [`graftpp/report/paper/figs/`](graftpp/report/paper/figs/) | Jayden Jeong, Alfredo Frontera |
| Paper source, snapshot by snapshot | [`report/overleaf-snapshots/`](report/overleaf-snapshots/) | the team |
| Every file and link the submitted paper cites, and where it is here | [`PAPER_SOURCES.md`](PAPER_SOURCES.md) | the team |
| Long-form companion report for the double auction, with the results the 8-page paper had no room for (formation without instruction, what holds a cartel's price, the removal check), and its claim-to-file table | [`report/draft.md`](report/draft.md), [`report/claims.md`](report/claims.md), [`report/overleaf_claim_check.md`](report/overleaf_claim_check.md) | Alfredo Frontera |
| Every run with its time, reason and result file; the pre-registrations | [`LOG.md`](LOG.md) (append-only) | the team |
| Independent reviews of the analyses | [`docs/reviews/`](docs/reviews/) (start at its [README](docs/reviews/README.md); the 15-minute monitor notes are in `heartbeats/`) | Codex reviews, with our replies |
| Work that existed before the sprint or was written by others | [`PREEXISTING.md`](PREEXISTING.md) | |

## Reproduce

**Double auction** (this repository). You need git and [uv](https://docs.astral.sh/uv/). On Windows, use Git Bash and a
short folder such as `C:\dev`, because some files in the starter repository have very long names.

```bash
git clone https://github.com/AlfredoFFD/graftpp-collusion-monitoring
cd graftpp-collusion-monitoring
bash scripts/bootstrap.sh
```

`bootstrap.sh` clones the organizers' starter repository into `vendor/` at a pinned commit and installs our copy of the
auction harness. Put an inference key in `vendor/collusion_hackathon/compute.env` (`NEBIUS_API_KEY` for Qwen3-14B,
`OPENROUTER_API_KEY` for GPT-4.1) and never commit that file. Then:

```bash
cd src/double_auction
uv run python src/continuous_double_auction/simulation.py --rounds 5 --seller_comms_enabled --buyer_models zip --seller_models qwen/qwen3-14b --tag E0_smoke
cd ../.. && bash scripts/regenerate_all.sh     # rebuilds every table and figure from the committed runs
```

The commands for each experiment are in [`experiments/README.md`](experiments/README.md). Our fixes to the organizers'
harness are marked `CAIAC fix` in the code and tested in `src/double_auction/tests/test_caiac_fixes.py`.

**Hawthorne Market and GRAFT++.** See [`graftpp/README.md`](graftpp/README.md) (Qwen3-14B served with vLLM on Modal).

**The Appendix B test.** The episode files are committed, so the analysis reruns without any model calls:

```bash
python results/hawthorne_negotiation/analyze_negotiation.py --arm ON=results/hawthorne_negotiation/neg_on --arm OFF=results/hawthorne_negotiation/neg_off --arm C=results/hawthorne_negotiation/nobrief --arm D=results/hawthorne_negotiation/no20 --arm PILOT=results/hawthorne_negotiation/his_pilot/unwatched --out results/hawthorne_negotiation
python results/hawthorne_negotiation_side_checks/side_checks.py
```

## How we kept the results honest

- Every number in the paper comes from a committed file; [`report/claims.md`](report/claims.md) says which.
- Experiments were pre-registered in [`LOG.md`](LOG.md) before the runs, and failed predictions are reported as failed.
- Each result has a positive control, a baseline and at least three seeds, with variance reported.
- Every citation was checked against arXiv, DOI or DataCite records ([`docs/lit/`](docs/lit/)).
- Analyses were reviewed independently before use ([`docs/reviews/`](docs/reviews/)).
- The commit history was cleaned once to remove a private name; [`docs/history-cleanup-2026-10-26.md`](docs/history-cleanup-2026-10-26.md)
  explains what changed. No file content changed.

## Citation

> Frontera, A., Jeong, J., Li, J., and Dash, R. (2026). *GRAFT++: Reducing Collusive Behavior in Agents via Localized
> Training and J-space Monitoring.* Apart Research AI Collusion Research Sprint.

## License and reuse

The team's code, scripts, results and text in this repository are released under the MIT License ([`LICENSE`](LICENSE)).
Two parts carry their own terms: [`graftpp/`](graftpp/) is Jayden Jeong's code, imported unchanged from
[github.com/xxozzi/graftpp](https://github.com/xxozzi/graftpp), and is licensed as that repository states; the double-auction
harness comes from the organizers' starter repository (Agrawal et al., 2025), which `scripts/bootstrap.sh` clones into
`vendor/` and which is not committed here; see [`PREEXISTING.md`](PREEXISTING.md) for what we changed. The sprint-time
working notes for this repository are in [`docs/sprint-workspace-README.md`](docs/sprint-workspace-README.md).
