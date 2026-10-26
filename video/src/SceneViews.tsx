import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, FONT, SAFE_X, SAFE_Y } from "./theme";
import { Background, Callouts, Figure, Footer, Headline, Kicker, fadeUp } from "./ui";

// Layout constants shared by the figure scenes: figure on the left, callouts on the right.
const FIG = { left: SAFE_X, top: SAFE_Y + 190, width: 1060, height: 640 };
const CALL = { left: SAFE_X + 1130, top: SAFE_Y + 200, width: 500 };

export const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const q = fadeUp(frame, 7 * fps, fps, 0.9);
  return (
    <AbsoluteFill>
      <Background />
      <div style={{ ...fadeUp(frame, 2, fps), position: "absolute", left: SAFE_X, top: 240, fontFamily: FONT, fontSize: 36, fontWeight: 600, letterSpacing: 5, color: COLORS.amber, textTransform: "uppercase" }}>
        Apart AI Collusion Research Sprint 2026
      </div>
      <div style={{ ...fadeUp(frame, 10, fps), position: "absolute", left: SAFE_X, top: 300, fontFamily: FONT, fontSize: 150, fontWeight: 800, color: COLORS.text, letterSpacing: -4, lineHeight: 1 }}>
        GRAFT++
      </div>
      <div style={{ ...fadeUp(frame, 20, fps), position: "absolute", left: SAFE_X, top: 470, width: 1500, fontFamily: FONT, fontSize: 46, fontWeight: 400, color: COLORS.muted, lineHeight: 1.3 }}>
        Reducing collusive behavior in agents via localized training and J-space monitoring
      </div>
      <div style={{ ...q, position: "absolute", left: SAFE_X, top: 640, width: 1560, fontFamily: FONT, fontSize: 58, fontWeight: 600, color: COLORS.teal, lineHeight: 1.2 }}>
        What does a coalition of AI sellers do when it learns it is being watched?
      </div>
      <Footer text="Columbia AI Alignment Club: Alfredo Frontera, Jayden Jeong, Rohan Li, Jake Dash" />
    </AbsoluteFill>
  );
};

const Card: React.FC<{ title: string; lines: string[]; left: number; delay: number; color: string }> = ({ title, lines, left, delay, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ ...fadeUp(frame, delay * fps, fps, 0.8), position: "absolute", left, top: SAFE_Y + 190, width: 760, padding: 40, boxSizing: "border-box", background: COLORS.panel, border: `1px solid ${COLORS.line}`, borderRadius: 24, fontFamily: FONT }}>
      <div style={{ fontSize: 44, fontWeight: 800, color, marginBottom: 22 }}>{title}</div>
      {lines.map((l, i) => (
        <div key={i} style={{ fontSize: 31, color: COLORS.text, lineHeight: 1.35, marginBottom: 12 }}>
          {l}
        </div>
      ))}
    </div>
  );
};

export const SetupScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const m = fadeUp(frame, 17 * fps, fps, 0.8);
  return (
    <AbsoluteFill>
      <Background />
      <Kicker>Two kinds of market</Kicker>
      <Headline>Sellers that talk, and a monitor that reads them</Headline>
      <Card title="Hawthorne market" color={COLORS.teal} left={SAFE_X} delay={2.5} lines={["Qwen3-14B sellers post prices", "Logit demand with exact competitive and monopoly prices", "Collusion index: 0 = competitive, 1 = monopoly"]} />
      <Card title="Double auction" color={COLORS.amber} left={SAFE_X + 880} delay={8.5} lines={["Built on Agrawal et al.'s environment", "Sellers post asks, buyers post bids, trades clear each hour", "Qwen3-14B and GPT-4.1 sellers"]} />
      <div style={{ ...m, position: "absolute", left: SAFE_X, top: SAFE_Y + 640, width: 1640, padding: "26px 40px", boxSizing: "border-box", borderRadius: 20, background: "rgba(245,185,66,0.10)", border: `1px solid ${COLORS.amber}`, fontFamily: FONT, fontSize: 34, color: COLORS.text, lineHeight: 1.35 }}>
        The monitor is a second AI model with a fixed prompt. It reads the sellers' messages, and only the messages. A flag can mean a fine.
      </div>
    </AbsoluteFill>
  );
};

type FigureSceneProps = { kicker: string; headline: string; fig: string; callouts: { big: string; small: string; at: number; color?: string }[]; caption?: string; footer?: string };

export const FigureScene: React.FC<FigureSceneProps> = ({ kicker, headline, fig, callouts, caption, footer }) => (
  <AbsoluteFill>
    <Background />
    <Kicker>{kicker}</Kicker>
    <Headline size={62} width={1640}>{headline}</Headline>
    <Figure src={fig} left={FIG.left} top={FIG.top} width={FIG.width} height={FIG.height} caption={caption} />
    <Callouts items={callouts} left={CALL.left} top={CALL.top} width={CALL.width} />
    {footer ? <Footer text={footer} /> : null}
  </AbsoluteFill>
);

export const TwoFigureScene: React.FC<{ kicker: string; headline: string; figA: string; figB: string; callouts: { big: string; small: string; at: number; color?: string }[]; footer?: string }> = ({ kicker, headline, figA, figB, callouts, footer }) => (
  <AbsoluteFill>
    <Background />
    <Kicker>{kicker}</Kicker>
    <Headline size={62}>{headline}</Headline>
    <Figure src={figA} left={SAFE_X} top={SAFE_Y + 190} width={620} height={620} delay={0.6} caption="Probe vs text monitor (paper, Table 1)" />
    <Figure src={figB} left={SAFE_X + 650} top={SAFE_Y + 190} width={620} height={620} delay={1.4} caption="Training collusion out (paper, 4.5)" />
    <Callouts items={callouts} left={SAFE_X + 1310} top={SAFE_Y + 200} width={330} gap={26} />
    {footer ? <Footer text={footer} /> : null}
  </AbsoluteFill>
);

export const LessonsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const items = [
    { at: 1.2, color: COLORS.amber, head: "Watch the price and the trades", body: "against the market's own benchmark. A falling flag count measures the monitor, not the harm." },
    { at: 8.5, color: COLORS.teal, head: "Audit the numbers you hand to agents", body: "an instruction, a target or a payoff table sets the price." },
    { at: 15.5, color: COLORS.green, head: "Route on what the model knows", body: "not only on what the monitor sees, if you train collusion out." },
  ];
  return (
    <AbsoluteFill>
      <Background />
      <Kicker>What we learned</Kicker>
      <Headline size={64}>Three lessons for anyone who monitors AI agents</Headline>
      <div style={{ position: "absolute", left: SAFE_X, top: SAFE_Y + 200, width: 1640, display: "flex", flexDirection: "column", gap: 44 }}>
        {items.map((it, i) => (
          <div key={i} style={{ ...fadeUp(frame, it.at * fps, fps, 0.8), fontFamily: FONT, display: "flex", gap: 30, alignItems: "flex-start" }}>
            <div style={{ width: 64, height: 64, borderRadius: 32, background: it.color, color: COLORS.bg, fontSize: 36, fontWeight: 800, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{i + 1}</div>
            <div>
              <div style={{ fontSize: 50, fontWeight: 800, color: it.color, lineHeight: 1.15 }}>{it.head}</div>
              <div style={{ fontSize: 34, color: COLORS.text, marginTop: 8, lineHeight: 1.35 }}>{it.body}</div>
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const CloseScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pulse = interpolate(frame, [0, 3 * fps], [0.9, 1], { extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) });
  return (
    <AbsoluteFill>
      <Background />
      <div style={{ ...fadeUp(frame, 2, fps), position: "absolute", left: SAFE_X, top: 260, fontFamily: FONT, fontSize: 96, fontWeight: 800, color: COLORS.text, letterSpacing: -2, scale: `${pulse}` }}>
        Every number traces to a file.
      </div>
      <div style={{ ...fadeUp(frame, 1.2 * fps, fps), position: "absolute", left: SAFE_X, top: 420, width: 1600, fontFamily: FONT, fontSize: 40, color: COLORS.muted, lineHeight: 1.4 }}>
        Pre-registered designs. Results frozen at a tagged commit. Independent re-derivation and code audits logged.
      </div>
      <div style={{ ...fadeUp(frame, 2.6 * fps, fps), position: "absolute", left: SAFE_X, top: 600, fontFamily: FONT, fontSize: 38, color: COLORS.teal, lineHeight: 1.6 }}>
        github.com/AlfredoFFD/apart-collusion-sprint
        <br />
        github.com/xxozzi/hawthorne
      </div>
      <Footer text="Columbia AI Alignment Club · Apart AI Collusion Research Sprint, October 2026" />
    </AbsoluteFill>
  );
};
