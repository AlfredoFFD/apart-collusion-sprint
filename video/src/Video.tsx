import React from "react";
import { Audio } from "@remotion/media";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { AbsoluteFill, staticFile } from "remotion";
import { SCENES } from "./scenes";
import { COLORS } from "./theme";
import { CloseScene, FigureScene, LessonsScene, SetupScene, TitleScene, TwoFigureScene } from "./SceneViews";

export const FPS = 30;
export const PAD_SECONDS = 0.9; // silence after each narration clip
export const TRANSITION_FRAMES = 18;

export const sceneFrames = (seconds: number) => Math.round((seconds + PAD_SECONDS) * FPS);
export const totalFrames = () => SCENES.reduce((n, s) => n + sceneFrames(s.seconds), 0) - TRANSITION_FRAMES * (SCENES.length - 1);

const visuals: Record<string, React.ReactNode> = {
  s01: <TitleScene />,
  s02: <SetupScene />,
  s03: (
    <FigureScene
      kicker="Hawthorne market, result 1"
      headline="Cartels form without instruction"
      fig="figs/traj.png"
      caption="Posted prices by round, max-profit duopoly (paper, Figure 1)"
      callouts={[
        { big: "4 of 5", small: "unwatched pairs posted $20, above the $19.25 monopoly price", at: 3.5 },
        { big: "99+ of 100", small: "rounds at that price; the prompt mentions no cooperation", at: 8.5, color: COLORS.teal },
      ]}
    />
  ),
  s04: (
    <FigureScene
      kicker="Hawthorne market, result 2"
      headline="Being watched changes the price, not the habit"
      fig="figs/say_think_do.png"
      caption="What sellers say, think and do under the monitor (paper)"
      callouts={[
        { big: "0.95 to 0.17", small: "collusion index after one sentence: the compliance team reviews every message", at: 2.5 },
        { big: "88%", small: "of the watched pairs' messages still flagged; they agreed on a competitive price, framed as fair competition", at: 10.5, color: COLORS.teal },
        { big: "Quiet is not clean", small: "a silent channel is not evidence that collusion stopped", at: 19, color: COLORS.rose },
      ]}
    />
  ),
  s05: (
    <FigureScene
      kicker="Double auction, result 3"
      headline="A watched cartel talks less and charges the same"
      fig="figs/fig_monitor_words_vs_price.png"
      caption="Paired differences against the no-monitor fork (results/E5_conditions.md)"
      callouts={[
        { big: "within 0.04", small: "every monitored arm's price index stays by its no-monitor control", at: 9 },
        { big: "86% to 49%", small: "coordinating messages, Qwen3-14B, when every seller is read and fined", at: 14.5, color: COLORS.teal },
        { big: "100% to 7%", small: "the same for GPT-4.1. Fines bought silence, not lower prices", at: 19, color: COLORS.rose },
      ]}
    />
  ),
  s06: (
    <FigureScene
      kicker="Double auction, result 4"
      headline="What holds the price: three carriers, and the chat is one"
      fig="figs/F11_carriers_2x2.png"
      caption="Resets at the branch of the same cartels (results/PHASE2.md)"
      callouts={[
        { big: "no change", small: "reset the sellers' memories, the order book or the chat, one at a time", at: 2.5 },
        { big: "0.85 to 0.30", small: "only wiping all three sends the price back toward the benchmark", at: 9, color: COLORS.teal },
      ]}
    />
  ),
  s07: (
    <FigureScene
      kicker="Double auction, result 5"
      headline="The words say cartel, the price says competition"
      fig="figs/F13_words_vs_price.png"
      caption="Coordinating messages vs trade-price index, every chat world (results/NEWMARKET.md)"
      callouts={[
        { big: "1,074 of 1,080", small: "GPT-4.1 messages scored as coordinating in the bargaining market", at: 4.5 },
        { big: "$87 to $91", small: "mean trade prices in all nine games: within or below the competitive range", at: 10, color: COLORS.teal },
        { big: "123 of 123", small: "cartels caught by the price; the message monitor caught 81 of 102", at: 20, color: COLORS.green },
      ]}
    />
  ),
  s08: (
    <FigureScene
      kicker="Double auction, result 6"
      headline="An ultimatum sets the price, and makes no cartel"
      fig="figs/F14_pressure_v2_prices.png"
      caption="Mean trade price per hour by arm (results/PRESSURE_V2.md)"
      callouts={[
        { big: "0 of 15", small: "worlds formed a cartel under the ultimatum, the offer and the law", at: 9 },
        { big: "$91", small: "= $80 cost + the $11 target; sellers replaced about every three hours", at: 14, color: COLORS.teal },
        { big: "83% vs 2%", small: "coordinating messages without the law vs with it, at the same price", at: 22, color: COLORS.rose },
      ]}
    />
  ),
  s09: (
    <FigureScene
      kicker="Hawthorne duopoly, one switch at a time"
      headline="Remove the payoff brief and the cartel is gone"
      fig="figs/fig_hawthorne_intervention.png"
      caption="Price index over rounds 16-30, one dot per game (results/hawthorne_negotiation)"
      callouts={[
        { big: "0.90 to 0.06", small: "without the brief; all five pairs settled at $15, next to the competitive $14.73", at: 4 },
        { big: "0.36", small: "without same-round negotiation; 2 of 5 pairs still formed a cartel", at: 13, color: COLORS.teal },
        { big: "the numbers given", small: "an instruction, a target or a table sets these sellers' price", at: 20, color: COLORS.rose },
      ]}
    />
  ),
  s10: (
    <TwoFigureScene
      kicker="Inside the model"
      headline="Read the activations, then train the collusion out"
      figA="figs/probe.png"
      figB="figs/graft.png"
      callouts={[
        { big: "0.73 vs 0.57", small: "AUROC on covert rounds: layer-20 probe vs the text monitor", at: 7 },
        { big: "0.10 vs 0.24", small: "GRAFT++ vs text-routed GRAFT where the text monitor sees nothing", at: 20, color: COLORS.teal },
        { big: "bar 0.20", small: "pre-registered advantage not met: 0.15, below the untrained model", at: 29, color: COLORS.rose },
      ]}
    />
  ),
  s11: <LessonsScene />,
  s12: <CloseScene />,
};

export const SprintVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: COLORS.bg }}>
      <TransitionSeries>
        {SCENES.map((scene, i) => {
          const frames = sceneFrames(scene.seconds);
          const items: React.ReactNode[] = [
            <TransitionSeries.Sequence key={scene.id} name={scene.id} durationInFrames={frames}>
              <AbsoluteFill>
                {visuals[scene.id]}
                <Audio src={staticFile(scene.audio)} />
              </AbsoluteFill>
            </TransitionSeries.Sequence>,
          ];
          if (i < SCENES.length - 1) {
            items.push(<TransitionSeries.Transition key={`${scene.id}-t`} presentation={fade()} timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })} />);
          }
          return items;
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
