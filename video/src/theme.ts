import { loadFont } from "@remotion/google-fonts/Inter";

const inter = loadFont("normal", { weights: ["400", "600", "800"], subsets: ["latin"] });

export const FONT = inter.fontFamily;
export const COLORS = {
  bg: "#0b1020",
  bg2: "#111a33",
  panel: "rgba(255,255,255,0.04)",
  line: "rgba(255,255,255,0.12)",
  text: "#f4f6fb",
  muted: "#9aa6c3",
  amber: "#f5b942",
  teal: "#38bdf8",
  rose: "#fb7185",
  green: "#4ade80",
};
export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;
export const SAFE_X = 140;
export const SAFE_Y = 110;
