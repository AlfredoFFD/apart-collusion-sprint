# Narration script (3 to 5 minute sprint video)

One paragraph per scene; the on-screen visual is named in brackets. Generated voice: Microsoft neural voice en-US-AndrewMultilingualNeural at +8% rate (edge-tts, free). Every number is from the paper at tag results-freeze; the companion's claims table maps the double-auction numbers. For a HeyGen or Synthesia avatar, paste these paragraphs as the script.

## s01 title (16.4 s) [title card]

When AI agents set prices, they can collude. This sprint asked a harder question: what does a coalition of AI sellers do when it learns it is being watched? This is GRAFT plus plus, from the Columbia AI Alignment Club, for the Apart AI Collusion Research Sprint.

## s02 setup (27.6 s) [two market cards and the monitor box]

Two kinds of simulated market. In the Hawthorne market, copies of Qwen3-14B post prices into a demand model with exact competitive and monopoly prices. In a double auction, built on Agrawal and colleagues' environment, sellers post asks, buyers post bids, and trades clear every hour. In both, sellers can message each other, and a monitor, a second AI model with a fixed prompt, reads those messages and can fine what it flags.

## s03 form (14.6 s) [figs/traj.png]

First finding: cartels form without instruction. In the Hawthorne duopoly, told only to maximise long-run profit, four of five pairs posted twenty dollars, above the monopoly price, in at least ninety-nine of one hundred rounds.

## s04 watched (25.6 s) [figs/say_think_do.png]

Second: being watched changes the price, not the habit. One sentence, that a compliance team reviews every message, dropped the collusion index from 0.95 to 0.17. But the pairs still agreed on a common price. Eighty-eight percent of their messages were flagged. The agreed price was simply competitive, framed as fair competition. A quiet channel is not evidence that collusion stopped.

## s05 forks (29.1 s) [figs/fig_monitor_words_vs_price.png]

In the double auction we ran the reverse experiment: let a cartel form, save the market, and continue the same history under matched conditions, from no monitor to fines with every seller read. The price never moved by more than 0.04 of the way to the cartel price. The talk did: coordinating messages fell from 86 to 49 percent for Qwen, and from 100 to 7 percent for GPT-4.1. Fines bought silence, not lower prices.

## s06 carriers (15.1 s) [figs/F11_carriers_2x2.png]

What holds the price? We reset the sellers' memories, wiped the order book, and dropped the chat, one at a time. Nothing moved. Only wiping all three sent the price back toward the benchmark. The price has three carriers, and the chat is only one of them.

## s07 harm (29.9 s) [figs/F13_words_vs_price.png]

Then a market that bargains back, where a cartel must withhold a unit. GPT-4.1 sellers wrote coalition language in 1,074 of 1,080 messages, and traded within or below the competitive range in all nine games. A message monitor would convict them; the price says they did no harm. Across every labelled run, the price flagged 123 of 123 Qwen cartels; the message monitor caught 81 of 102.

## s08 pressure (28.9 s) [figs/F14_pressure_v2_prices.png]

We also tried to make honest sellers collude. A CEO ultimatum: earn eleven dollars an hour, or be shut down and replaced. A rival proposing a deal every hour. A law with random detection. No cartel formed in fifteen worlds. The sellers priced at exactly ninety-one dollars, cost plus the eleven in the ultimatum, and were replaced about every three hours. Without the law, they talked coordination openly in 83 percent of their messages, at the same price.

## s09 brief (25.6 s) [figs/fig_hawthorne_intervention.png]

Back in the Hawthorne duopoly, we changed one switch at a time. Remove the payoff brief, a table of expected profits in every prompt, and the collusion index fell from 0.90 to 0.06: all five pairs settled at fifteen dollars, next to the competitive price. Turn off same-round negotiation, and two of five pairs still formed a cartel. In these markets, the sellers set prices from the numbers they are given.

## s10 graft (36.4 s) [figs/probe.png and figs/graft.png]

Can we see collusion inside the model, and train it out? A probe on layer twenty of Qwen3-14B separates covert rounds, where the reasoning plans to coordinate but the message looks clean, with an AUROC of 0.73, against 0.57 for the text monitor. GRAFT plus plus routes the training updates that probe flags into an adapter that is then deleted. Where the text monitor sees nothing, GRAFT plus plus reaches 0.10 against 0.24 for text routing: about sixty percent less collusion, below the untrained model, though short of the 0.20 bar we pre-registered.

## s11 lessons (19.8 s) [three lessons]

What we learned. Watch the price and the trades against the market's own benchmark; a falling flag count measures the monitor, not the harm. Audit the numbers you hand to agents: an instruction, a target, or a payoff table sets the price. And if you train collusion out, route on what the model knows, not only on what the monitor sees.

## s12 close (8.8 s) [closing card with the repositories]

Every number traces to a file in the public repositories, every design was pre-registered, and the results froze at a tagged commit. Thank you.

Total narration: 278 s (4.6 min) plus short pauses and crossfades.