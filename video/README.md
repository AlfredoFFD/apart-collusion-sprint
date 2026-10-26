# Sprint video (Remotion)

A 3 to 5 minute narrated explainer of the paper, built from the committed figures and a free neural voice. Every number spoken or shown comes from the paper at tag `results-freeze`.

- `tools/make_audio.py`: the narration (one clip per scene) via edge-tts (Microsoft neural voice, no account); writes `public/audio/*.mp3` and `src/scenes.ts`. Run `py tools/make_audio.py --force` to regenerate.
- `src/Video.tsx`: the scene list (headlines, figures, callouts and their timings); `src/SceneViews.tsx` and `src/ui.tsx`: the scene components; `src/theme.ts`: colours and font.
- `public/figs/`: copies of `results/figures/*`, `results/paper_figures/*` and the paper's Hawthorne figures from `github.com/xxozzi/hawthorne`.
- `SCRIPT.md`: the narration text, for an avatar tool if wanted.

Build: `npm i`, then `npx remotion render SprintVideo out/graftpp_sprint_video.mp4 --codec=h264`. Preview: `npx remotion studio`. `node_modules/` and `out/` are not committed.
