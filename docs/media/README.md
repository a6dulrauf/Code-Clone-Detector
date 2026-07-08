# Media capture plan

This project's screenshots/GIFs are captured live by the repo owner on a machine
with a display (they can't be generated in a headless environment). This file is
the checklist for producing them. The main `README.md` already links to the three
filenames below — drop the finished files in this directory with these exact
names and the links will resolve with no further edits.

## 1. `web.gif`

1. `make web` (or `make docker`) to start the Django app locally.
2. Open the login page — note the demo-credentials hint banner.
3. Log in with `demo` / `demo12345`.
4. Go to **My Projects**, open the seeded **demo-comparison** project, and
   click **TEST PLAGIARISM** — no upload needed, it's pre-loaded with
   `samples/Original.java` and `samples/NearClone.java`.
5. Let the recording run until the numeric similarity result is visible on screen.
6. Record with macOS screen recording (Cmd-Shift-5) or `ffmpeg`, then convert to
   an optimized GIF with Gifski or `ffmpeg`'s palette-based GIF pipeline. Keep it
   short (~10-20s) and under a few MB.
7. Save as `docs/media/web.gif`.

## 2. `desktop.gif`

1. `make desktop` to launch the Tkinter app (requires system Tk — see README).
2. Browse to two sample folders (e.g. `samples/` files or a small project pair).
3. Click **TEST PLAGIARISM** and let the result/plot render.
4. Record the interaction end-to-end (window open → browse → run → result).
5. Save as `docs/media/desktop.gif`.

## 3. `cli.gif`

1. `make demo` in a terminal with a reasonably-sized font (for readability).
2. Record the terminal session from invocation through both printed results.
3. A terminal recorder (asciinema + agg, or a plain screen recording) works fine.
4. Save as `docs/media/cli.gif`.

## Notes

- Do not fabricate or hand-draw placeholder images — leave the links pointing at
  these filenames until the real captures are dropped in; GitHub will just show
  a broken-image icon in the meantime, which is expected and honest.
- Keep files reasonably small (a few MB each) so the README stays fast to load.
- If a static screenshot is easier than a GIF for a given interface, a `.png`
  with the same base name is an acceptable substitute — just update the
  extension in `README.md` to match.
