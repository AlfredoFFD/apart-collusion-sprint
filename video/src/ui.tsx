import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, FONT, SAFE_X, SAFE_Y } from "./theme";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

export const fadeUp = (frame: number, start: number, fps: number, dur = 0.6) => {
  const t = interpolate(frame, [start, start + dur * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return { opacity: t, translate: `0px ${(1 - t) * 40}px` };
};

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: `radial-gradient(1200px 800px at 20% 10%, ${COLORS.bg2} 0%, ${COLORS.bg} 60%)` }}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${COLORS.line} 1px, transparent 1px), linear-gradient(90deg, ${COLORS.line} 1px, transparent 1px)`,
          backgroundSize: "120px 120px",
          opacity: 0.35,
          translate: `${-(frame * 0.15) % 120}px 0px`,
        }}
      />
    </AbsoluteFill>
  );
};

export const Kicker: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = COLORS.amber }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ ...fadeUp(frame, 0, fps), position: "absolute", left: SAFE_X, top: SAFE_Y, fontFamily: FONT, fontSize: 30, fontWeight: 600, letterSpacing: 4, textTransform: "uppercase", color }}>
      {children}
    </div>
  );
};

export const Headline: React.FC<{ children: React.ReactNode; top?: number; size?: number; width?: number }> = ({ children, top = SAFE_Y + 60, size = 72, width = 1640 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ ...fadeUp(frame, 4, fps), position: "absolute", left: SAFE_X, top, width, fontFamily: FONT, fontSize: size, fontWeight: 800, lineHeight: 1.1, color: COLORS.text, letterSpacing: -1 }}>
      {children}
    </div>
  );
};

export const Figure: React.FC<{ src: string; left: number; top: number; width: number; height: number; delay?: number; caption?: string }> = ({ src, left, top, width, height, delay = 0.5, caption }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = fadeUp(frame, delay * fps, fps, 0.8);
  const zoom = interpolate(frame, [0, 60 * fps], [1, 1.04], { extrapolateRight: "clamp" });
  return (
    <div style={{ ...a, position: "absolute", left, top, width, height, background: "#ffffff", borderRadius: 18, boxShadow: "0 30px 80px rgba(0,0,0,0.45)", overflow: "hidden", border: `1px solid ${COLORS.line}` }}>
      <Img src={staticFile(src)} style={{ width: "100%", height: caption ? "calc(100% - 44px)" : "100%", objectFit: "contain", padding: 14, boxSizing: "border-box", scale: `${zoom}` }} />
      {caption ? <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 44, fontFamily: FONT, fontSize: 22, color: "#333", background: "#f3f4f8", display: "flex", alignItems: "center", paddingLeft: 18 }}>{caption}</div> : null}
    </div>
  );
};

export type Callout = { big: string; small: string; at: number; color?: string };

export const Callouts: React.FC<{ items: Callout[]; left: number; top: number; width?: number; gap?: number }> = ({ items, left, top, width = 520, gap = 34 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ position: "absolute", left, top, width, display: "flex", flexDirection: "column", gap }}>
      {items.map((c, i) => {
        const a = fadeUp(frame, c.at * fps, fps, 0.7);
        return (
          <div key={i} style={{ ...a, fontFamily: FONT, borderLeft: `6px solid ${c.color ?? COLORS.amber}`, paddingLeft: 22 }}>
            <div style={{ fontSize: 64, fontWeight: 800, color: c.color ?? COLORS.amber, lineHeight: 1.05, letterSpacing: -1 }}>{c.big}</div>
            <div style={{ fontSize: 30, color: COLORS.text, marginTop: 8, lineHeight: 1.3 }}>{c.small}</div>
          </div>
        );
      })}
    </div>
  );
};

export const Footer: React.FC<{ text: string }> = ({ text }) => (
  <div style={{ position: "absolute", left: SAFE_X, bottom: 56, fontFamily: FONT, fontSize: 24, color: COLORS.muted }}>{text}</div>
);
