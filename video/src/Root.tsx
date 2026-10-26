import React from "react";
import { Composition } from "remotion";
import { FPS, SprintVideo, totalFrames } from "./Video";
import { HEIGHT, WIDTH } from "./theme";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="SprintVideo" component={SprintVideo} durationInFrames={totalFrames()} fps={FPS} width={WIDTH} height={HEIGHT} />
    </>
  );
};
