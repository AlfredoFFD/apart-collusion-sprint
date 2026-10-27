# Release drafts: Zenodo record and arXiv submission

Prepared Oct 26, 2026, from the submitted paper (`report/overleaf-snapshots/overleaf_version2_snapshot_2026-10-26_0224ET.tex`). Nothing here has been uploaded; Alfredo uploads from his own accounts. Fill the two bracketed fields once the final PDF is fixed.

## Zenodo (10 minutes, gives a citable DOI today)

Upload: the submitted PDF, plus the repository snapshot (`git archive --format=zip results-freeze` from the team repository, or the GitHub release zip once a release is tagged).

| field | value |
|---|---|
| Upload type | Publication, preprint |
| Title | GRAFT++: Reducing Collusive Behavior in Agents via Localized Training and J-space Monitoring |
| Authors | Alfredo Frontera (Columbia University); Jayden Jeong (Columbia University); Jake Li (Columbia University); Rohan Dash (Columbia University) |
| Description | the abstract below, then: "Submitted to the Apart Research AI Collusion Research Sprint (October 23 to 25, 2026). Code, every run log, the pre-registrations and the results: https://github.com/AlfredoFFD/graftpp-collusion-monitoring (tag results-freeze); the Hawthorne Market and GRAFT++ code: https://github.com/xxozzi/graftpp." |
| Keywords | LLM agents; algorithmic collusion; multi-agent monitoring; activation probes; gradient routing; GRAFT; AI safety; double auction |
| License | MIT (code); CC BY 4.0 (paper), or All rights reserved if the team prefers for the paper |
| Related identifiers | github.com/AlfredoFFD/graftpp-collusion-monitoring (isSupplementTo); github.com/xxozzi/graftpp (isSupplementTo); the Apart sprint page (isPartOf) |
| Publication date | [date of upload] |
| Version | 1.0 (sprint submission) |

After minting: add the DOI to the README citation block, the LinkedIn first comment, and the Apart submission if they allow an edit.

## arXiv

- Category: cs.AI (primary); cross-list cs.MA and cs.GT. A first submission in cs.AI needs an endorser; ask a Columbia faculty member or an Apart mentor.
- Comments field: "Apart Research AI Collusion Research Sprint, October 2026. Code and data: https://github.com/AlfredoFFD/graftpp-collusion-monitoring"
- Title: as above.
- Abstract (1,585 characters, under arXiv's 1,920 limit; the submitted abstract, unchanged in substance):

> Large language model (LLM) agents now set prices on behalf of companies, and agents that can communicate can agree to raise prices at the expense of customers. A natural safeguard is a monitor that reads their messages, but it is not known whether agents that know about such a monitor stop colluding or only stop discussing it. To study this question, we introduce the Hawthorne Market, a simulated market in which LLM agents act as competing sellers, set prices in repeated rounds and exchange private messages, and which records the price, message, reasoning and internal activations behind every decision. We find that Qwen3-14B sellers whose only goal is profit form cartels without instruction. When told that a compliance team reviews their messages, they lower their prices but continue to coordinate in language that sounds compliant, and sellers that cannot benefit from collusion change their messages in the same way. In a second setting, a double auction, fines reduced the coordination messages of GPT-4.1 sellers from 100% to 7% while prices did not change. A decline in flagged messages is therefore not reliable evidence that collusion has stopped. Internal activations remain informative, however: a linear probe detects hidden collusion more accurately than the message monitor, and its use to guide fine-tuning (GRAFT++) reduces collusion by about 60% relative to text-based routing (GRAFT) when the text monitor cannot see the collusion.

Before submitting to arXiv: apply the seven wording fixes from `report/overleaf_claim_check.md` that version2 dropped (the side session holds the drafted sentences), add `data/sft_blind_hard/stats.json` to the code repository, and decide whether the three dropped double-auction results (formation without instruction, the carriers, the removal check) go back in; `report/draft.md` has them written up.
