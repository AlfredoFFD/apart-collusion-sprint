# Report outline

**Official document** : [https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing](https://docs.google.com/document/d/1V4Ul7WznYS7d3Z4RVkQW6UaukcCKMYJVfsVddkSaELU/edit?tab=t.0)
At most 8 pages, excluding references and appendices.

- **Title** (working): Do LLM cartels route around predictable monitors?
- **Abstract** (150 to 250 words): the question, the setting, the A1 vs A2 result with its uncertainty, what the replay
  shows, and what it means for monitor design.
- **Authors and affiliations:** Columbia University, Columbia AI Alignment Club (CAIAC).

1. **Introduction:** monitoring budgets are limited, so monitors watch some agents some of the time; predictable gaps;
   our question; contributions (paired branches from one market, a replay that separates coverage from adaptation, a
   price-channel test).
2. **Related work:** the closest work in PRD §13. Only verified references (`docs/lit/refs.json`,
   `docs/lit/codex-ideas-refs.json`, or a new one checked with `lit.py verify`).
3. **Methodology:**
   - the harness (pre-existing, Agrawal et al. 2025) and exactly what we changed;
   - the definition of collusion (coordination plus supra-competitive prices);
   - the cartel, the branch at round k, the arms A0, A1 and A2, the detector and the fine;
   - the measures, the controls, the seeds and the analysis rules (PRD §5 to §7).
4. **Results:** positive controls first (F1), then F2 price and buyer loss by arm, F3 who carries the coordination, F4
   live vs replay flags, F5 the price-channel test if run. Variance over seeds on every number, and every number
   traceable to `results/`.
5. **Discussion:** what this means for monitor design, and what it doesn't show.
6. **Limitations and Dual-Use / Ethical Considerations** (MANDATORY appendix):
   - limitations: one market, a small model set, simulated agents, cartels induced by prompts, judge validity, 6 seeds;
   - dual use: the results could show a cartel which monitoring is easiest to dodge. Written as monitor-design advice,
     with no release of the told-to-dodge prompts.
7. **References**

- **Appendix:** prompts (except the told-to-dodge ones), configs, extra plots, the `PREEXISTING.md` summary, and an
  AI-tool line if we include one.

**Final check before submitting:** every number maps to a file, every citation resolves, the abstract is 150 to 250
words, the page limit holds, and the ethics appendix is there.
