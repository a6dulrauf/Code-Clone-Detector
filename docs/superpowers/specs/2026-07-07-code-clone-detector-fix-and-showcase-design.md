# Code Clone Detector — Fix & Showcase Design

**Date:** 2026-07-07
**Status:** Approved (design) — pending spec review
**Approach:** A — surgical fix-in-place (no refactor, no algorithm rewrite)

## 1. Goal

Take the existing Code Clone Detector (a revived university project) and get **all three
front-ends running correctly on macOS/Linux**, then make it **portfolio-ready**:

- A visitor can **click a live link** and see the web app detect code clones immediately.
- A visitor can **clone the repo and run any of the three parts locally in one command**.
- The three front-ends are the **console (CLI)**, the **desktop app (Tkinter)**, and the
  **web app (Django)**.

Portfolio hosting split: the user's **static portfolio stays on Vercel**; the **Django demo
is hosted on Render** and linked from the portfolio. Vercel was ruled out for the Django app
(serverless 250 MB function limit — the numpy/scipy/scikit-learn/pandas stack alone is 249 MB —
plus read-only filesystem incompatible with the app's SQLite + CSV + upload writes).

## 2. Background & current state

- **Language/stack:** Python 3.12, Django (upgraded 2.2 → 4.2 LTS), numpy, pandas, scipy,
  scikit-learn, nltk. Desktop adds Tkinter, Pillow, matplotlib.
- **Shared engine:** `com/vsa/` — n-gram metrics, Halstead metrics, cosine/euclidean distance,
  dataset handling, CSV generation, project/internal clone comparison. Consumed by all three
  front-ends.
- **Web:** Django app already boots and serves pages (SQLite, migrations applied). Auth-gated
  dashboard; login stores `username` in session; comparison flow writes uploads/CSVs to
  `projects/<user>/...` and `com/vsa/datasets/<user>/...`.
- **Desktop:** `com/vsa/gui/gui.py` has a `GUI()` entry under `__main__`; uses Tkinter + Pillow +
  matplotlib; loads images from `com/vsa/gui/images/`.
- **Console:** `com/vsa/Test.py` is dead code (commented-out body, broken imports, hardcoded
  Windows paths). No working CLI exists today.

### Known defects (discovered during exploration)

1. **Engine crash under modern libs:** `CosineDistance.test_palgiarism` does `float(result)` where
   `result` is a 2-D array `[[x]]` from `sklearn.cosine_similarity`; modern numpy raises
   `TypeError: only 0-dimensional arrays can be converted to Python scalars`. Same pattern likely
   in `EuclideanDistance`. **This breaks the web project-comparison path too.**
2. **Hardcoded Windows paths** across the engine and GUI (e.g. Halstead operators file path, GUI
   image paths). Break on macOS/Linux/containers.
3. **`SyntaxWarning`s:** `is not ''` string comparisons and invalid escape sequences (`'\A'`) in
   several modules.
4. **Filesystem writes** target project-relative dirs that must exist and be writable; needs a
   configurable base so it works in a container and on Render's persistent disk.

## 3. Architecture

```
                       ┌─────────────────────────┐
                       │   Shared engine (com/vsa)│
                       │  n-gram · Halstead ·     │
                       │  cosine/euclidean · CSV  │
                       └─────────────┬────────────┘
             ┌───────────────────────┼───────────────────────┐
             │                       │                       │
      ┌──────▼──────┐        ┌───────▼───────┐        ┌──────▼──────┐
      │  CLI        │        │  Desktop      │        │  Web        │
      │  cli.py     │        │  Tkinter GUI  │        │  Django     │
      │  (argparse) │        │  desktop.py   │        │  gunicorn   │
      └─────────────┘        └───────────────┘        └──────┬──────┘
                                                             │
                                                    ┌────────▼────────┐
                                                    │ Render (Docker) │
                                                    │ live demo URL   │
                                                    └─────────────────┘
```

**Principle:** fix the engine once; all three front-ends benefit. Front-ends are thin adapters
over the same engine API.

## 4. Detailed design

### 4.1 Engine repair (foundation)

- **Scalar extraction:** In `CosineDistance` and `EuclideanDistance`, return a proper Python float
  from the sklearn/scipy result (e.g. `float(result[0][0])` / `float(np.ravel(result)[0])`) instead
  of `float(<2-D array>)`.
- **Path independence:** Replace hardcoded Windows paths with module-relative resolution
  (`os.path.dirname(__file__)` or a project `BASE_DIR`). Applies to the Halstead operators data
  file and GUI image assets.
- **Configurable write root:** Introduce a single helper (or env var, e.g. `CCD_DATA_DIR`) that all
  write paths (uploaded files, generated CSVs, temp datasets) resolve against; defaults to a
  project-local `var/` (git-ignored) so it works locally, in Docker, and on Render's disk.
- **Warning cleanup:** Fix `is not ''` → `!= ''` and escape-sequence warnings **only in files we
  touch** for the above (surgical, not a sweep).
- **Verification:** add `tests/test_engine_smoke.py` (pytest) asserting a clone pair scores above a
  threshold and an unrelated pair scores below it, plus the previously-crashing cosine path now
  returns a float.

### 4.2 Console — CLI + demo

- New `cli.py` at repo root, argparse subcommands:
  - `compare A.java B.java [--ngram N]` — prints n-gram cosine similarity, Halstead metrics, and a
    clone verdict (threshold-based label).
  - `compare-projects DIR_A DIR_B [--ngram N]` — project-level similarity.
  - `demo` — runs against bundled `samples/` with zero arguments and prints results for a
    clone pair and a non-clone pair.
- Bundle `samples/`: `Original.java`, `NearClone.java` (renamed vars / minor edits), `Unrelated.java`.
- Output is plain, readable console text (scores as percentages + verdict).

### 4.3 Desktop — Tkinter

- Add `Pillow` + `matplotlib` to the environment; document the system Tk requirement
  (`python-tk` / bundled with python.org builds; miniforge needs `tk`).
- Fix GUI image paths to load module-relative from `com/vsa/gui/images/`.
- Resolve Python 3.12 / Tk issues surfaced at launch; ensure matplotlib uses a Tk-compatible backend
  when embedded, and does not force a headless backend.
- Launcher: `python desktop.py` (thin wrapper importing and running the GUI) and `make desktop`.
- Not hostable → captured as **screenshots + a GIF** for the README.

### 4.4 Web — Django + demo polish

- **Demo seeding:** a management command `python manage.py seed_demo` that (idempotently) creates a
  `demo` user with a known password and a **pre-loaded demo project** (sample files + any needed
  dataset dirs) so a logged-in visitor sees a real comparison result without setup.
- **Login page:** show the demo credentials prominently (banner/hint) on the deployed demo.
- **Production config (env-driven):** `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
  and DB/data paths read from environment; safe local defaults preserved. Keep SQLite.
- **Static/serving:** `gunicorn` as WSGI server, `WhiteNoise` for static files, `STATIC_ROOT` set,
  `collectstatic` in the build.
- Create the missing `static/` assets/dir as needed so `collectstatic` and templates resolve.

### 4.5 Packaging — local one-command + deploy

- **Dockerfile** (web): installs deps, downloads nltk data, runs `collectstatic`, launches gunicorn.
  Reused for local `docker run` and Render.
- **render.yaml:** Render web service from GitHub, persistent disk mounted for SQLite + uploads,
  env vars, `seed_demo` run on deploy.
- **Makefile** targets:
  - `make setup` — create `.venv`, install deps, download nltk data, `migrate`, `seed_demo`.
  - `make web` — run Django dev server.
  - `make cli ARGS="..."` / `make demo` — run the CLI / CLI demo.
  - `make desktop` — launch the Tkinter app.
  - `make test` — run pytest.
  - `make docker` — build + run the web container locally.
- **`.env.example`** documenting all env vars; **pinned `requirements.txt`** (web/CLI) and note on
  desktop-only extras (Pillow, matplotlib).

### 4.6 Portfolio polish — README

- Rewrite `README.md`:
  - One-line pitch + **live demo link** (Render) + **demo credentials**.
  - The three interfaces with a **GIF each** (web comparison, desktop app, CLI `demo` run).
  - **Architecture diagram** (the shared-engine → 3 front-ends → Render picture above, rendered).
  - "How it works": n-grams + Halstead metrics + cosine/euclidean similarity, in a few sentences.
  - Copy-paste local run: `make setup` then `make web` / `make cli` / `make desktop` / `make demo`.
  - Tech stack + honest note on Render free-tier cold start.

**Media capture plan (honest):** static screenshots of the web app can be captured programmatically;
desktop screenshots/GIFs require a live display and may be captured on the user's macOS session or
recorded by the user with provided steps. Where automated capture isn't reliable, the plan provides
exact recording steps and placeholder image slots so the README is complete and the media drops in.

## 5. Testing & verification

- **Engine:** pytest smoke test (clone > threshold, non-clone < threshold, cosine returns float).
- **CLI:** `make demo` runs clean and prints expected verdicts.
- **Web:** log in as `demo`, run the seeded project comparison, confirm a numeric result renders;
  `manage.py check` clean.
- **Desktop:** app launches, loads images, runs a comparison, shows a plot.
- **Container:** `make docker` serves the app locally; Render deploy reachable at its URL.

## 6. Non-goals (YAGNI)

- No algorithm rewrite or new detection techniques.
- No engine refactor beyond what's needed to run cross-platform/in a container.
- No migration off SQLite; no external DB service.
- No CI/CD beyond Render's auto-deploy from GitHub.
- No user-facing feature additions beyond demo seeding + demo credential display.

## 7. Risks & open items

- **Deeper engine breakage:** the project-comparison path (CSV alignment, `get_equal_dim_dataset`)
  may hide further version-compat issues beyond the cosine float bug; the smoke test + web
  verification will surface them, fixed under approach A as encountered.
- **Desktop on macOS:** Tk + matplotlib embedding can be finicky on 3.12/miniforge; may require a
  documented Tk install step.
- **Render cold start:** ~30–50s first hit on free tier; documented, optional keep-warm not in scope
  unless requested.
- **GIF automation:** desktop GIF likely needs a manual recording step (see media capture plan).
