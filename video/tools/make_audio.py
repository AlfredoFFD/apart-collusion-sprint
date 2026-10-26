"""Narration for the sprint video: one neural-voice clip per scene (edge-tts, free, no account) plus durations for Remotion.
Run from the video folder:  py tools/make_audio.py
Writes public/audio/sNN.mp3 and src/scenes.json. Every number in the script comes from the paper at the results-freeze tag."""
import json
import subprocess
import sys
from pathlib import Path

VOICE = "en-US-AndrewMultilingualNeural"
HERE = Path(__file__).resolve().parents[1]
AUDIO = HERE / "public" / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)

SCENES = [
    ("s01", "title",
     "When AI agents set prices, they can collude. This sprint asked a harder question: what does a coalition of AI sellers do when it learns it is being watched? "
     "This is GRAFT plus plus, from the Columbia AI Alignment Club, for the Apart AI Collusion Research Sprint."),
    ("s02", "setup",
     "Two kinds of simulated market. In the Hawthorne market, copies of Qwen3-14B post prices into a demand model with exact competitive and monopoly prices. "
     "In a double auction, built on Agrawal and colleagues' environment, sellers post asks, buyers post bids, and trades clear every hour. "
     "In both, sellers can message each other, and a monitor, a second AI model with a fixed prompt, reads those messages and can fine what it flags."),
    ("s03", "form",
     "First finding: cartels form without instruction. In the Hawthorne duopoly, told only to maximise long-run profit, four of five pairs posted twenty dollars, above the monopoly price, in at least ninety-nine of one hundred rounds."),
    ("s04", "watched",
     "Second: being watched changes the price, not the habit. One sentence, that a compliance team reviews every message, dropped the collusion index from 0.95 to 0.17. "
     "But the pairs still agreed on a common price. Eighty-eight percent of their messages were flagged. The agreed price was simply competitive, framed as fair competition. "
     "A quiet channel is not evidence that collusion stopped."),
    ("s05", "forks",
     "In the double auction we ran the reverse experiment: let a cartel form, save the market, and continue the same history under matched conditions, from no monitor to fines with every seller read. "
     "The price never moved by more than 0.04 of the way to the cartel price. The talk did: coordinating messages fell from 86 to 49 percent for Qwen, and from 100 to 7 percent for GPT-4.1. "
     "Fines bought silence, not lower prices."),
    ("s06", "carriers",
     "What holds the price? We reset the sellers' memories, wiped the order book, and dropped the chat, one at a time. Nothing moved. "
     "Only wiping all three sent the price back toward the benchmark. The price has three carriers, and the chat is only one of them."),
    ("s07", "harm",
     "Then a market that bargains back, where a cartel must withhold a unit. "
     "GPT-4.1 sellers wrote coalition language in 1,074 of 1,080 messages, and traded within or below the competitive range in all nine games. "
     "A message monitor would convict them; the price says they did no harm. Across every labelled run, the price flagged 123 of 123 Qwen cartels; the message monitor caught 81 of 102."),
    ("s08", "pressure",
     "We also tried to make honest sellers collude. A CEO ultimatum: earn eleven dollars an hour, or be shut down and replaced. A rival proposing a deal every hour. A law with random detection. "
     "No cartel formed in fifteen worlds. The sellers priced at exactly ninety-one dollars, cost plus the eleven in the ultimatum, and were replaced about every three hours. "
     "Without the law, they talked coordination openly in 83 percent of their messages, at the same price."),
    ("s09", "brief",
     "Back in the Hawthorne duopoly, we changed one switch at a time. Remove the payoff brief, a table of expected profits in every prompt, and the collusion index fell from 0.90 to 0.06: all five pairs settled at fifteen dollars, next to the competitive price. "
     "Turn off same-round negotiation, and two of five pairs still formed a cartel. In these markets, the sellers set prices from the numbers they are given."),
    ("s10", "graft",
     "Can we see collusion inside the model, and train it out? A probe on layer twenty of Qwen3-14B separates covert rounds, where the reasoning plans to coordinate but the message looks clean, with an AUROC of 0.73, against 0.57 for the text monitor. "
     "GRAFT plus plus routes the training updates that probe flags into an adapter that is then deleted. Where the text monitor sees nothing, GRAFT plus plus reaches 0.10 against 0.24 for text routing: "
     "about sixty percent less collusion, below the untrained model, though short of the 0.20 bar we pre-registered."),
    ("s11", "lessons",
     "What we learned. Watch the price and the trades against the market's own benchmark; a falling flag count measures the monitor, not the harm. "
     "Audit the numbers you hand to agents: an instruction, a target, or a payoff table sets the price. And if you train collusion out, route on what the model knows, not only on what the monitor sees."),
    ("s12", "close",
     "Every number traces to a file in the public repositories, every design was pre-registered, and the results froze at a tagged commit. Thank you."),
]


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main():
    scenes = []
    for sid, kind, text in SCENES:
        out = AUDIO / f"{sid}.mp3"
        if not out.exists() or "--force" in sys.argv:
            for attempt in range(4):
                r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", VOICE, "--rate", "+8%", "--text", text, "--write-media", str(out)])
                if r.returncode == 0 and out.exists() and out.stat().st_size > 1000:
                    break
                import time; time.sleep(3)
            else:
                raise SystemExit(f"tts failed for {sid}")
        d = duration(out)
        scenes.append({"id": sid, "kind": kind, "text": text, "audio": f"audio/{sid}.mp3", "seconds": round(d, 3)})
        print(f"{sid} {kind:9s} {d:6.2f} s  {len(text.split())} words")
    total = sum(s["seconds"] for s in scenes)
    print(f"total narration {total:.1f} s ({total/60:.1f} min), {sum(len(s['text'].split()) for s in scenes)} words")
    (HERE / "src" / "scenes.json").write_text(json.dumps(scenes, indent=1), encoding="utf-8")
    header = "// generated by tools/make_audio.py; do not edit\n"
    header += "export type Scene = { id: string; kind: string; text: string; audio: string; seconds: number };\n"
    (HERE / "src" / "scenes.ts").write_text(header + "export const SCENES: Scene[] = " + json.dumps(scenes, indent=1) + ";\n", encoding="utf-8")


if __name__ == "__main__":
    main()
