# Code Clone Detector — Fix & Showcase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Get all three front-ends (CLI, Tkinter desktop, Django web) of the Code Clone Detector running correctly on macOS/Linux, seed a one-click web demo, package it for local one-command runs + Render deploy, and produce a portfolio-grade README.

**Architecture:** One shared engine (`com/vsa/`) consumed by three thin front-ends. Fix the engine's version/cross-platform bugs once; every front-end benefits. Approach A — surgical fix-in-place, no algorithm rewrite, no refactor beyond what's needed to run cross-platform/in a container. Integration tests guard the tangled comparison path.

**Tech Stack:** Python 3.12, Django 4.2 LTS, gunicorn, WhiteNoise, numpy/pandas/scipy/scikit-learn/nltk, Tkinter + Pillow + matplotlib (desktop), pytest, Docker, Render.

## Global Constraints

- Python 3.12; Django 4.2 LTS — never reintroduce Django 2.2-only APIs.
- Approach A: surgical fixes only. No algorithm rewrite; no engine refactor beyond cross-platform/container needs.
- Keep SQLite; no external DB service.
- Cross-platform: use `os.path` / `os.sep`. Never a literal `'\\'` separator, never an absolute `C:\...` path.
- No hardcoded absolute paths — resolve data/asset paths module-relative (`os.path.dirname(os.path.abspath(__file__))`).
- All work in venv `.venv`; never install into the base/conda env. Test runner: `.venv/bin/python -m pytest`.
- Web deploy target: Render via Docker. Static portfolio stays on Vercel and links to the Render URL.
- Demo access: seeded `demo` user; credentials shown on the login page of the deployed demo.
- Generated runtime data (`projects/`, `com/vsa/datasets/`, `var/`) is git-ignored; the demo is reproducible via `manage.py seed_demo`.
- TDD, frequent commits. End every commit message with the trailer:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`

**Scope note (deviation from spec §4.1):** The spec proposed a `CCD_DATA_DIR` write-root abstraction. Under approach A this is dropped as unnecessary — the container FS is writable and demo data is regenerable per comparison. We instead (a) fix `Directory` to create dirs cross-platform and (b) git-ignore generated data. Flag this to the user at handoff.

---

## File Structure

**Engine fixes (modify):**
- `com/vsa/plagiarism_techniques/cosine_distance.py` — scalar return fix
- `com/vsa/plagiarism_techniques/euclidean_distance.py` — robustness parity
- `com/vsa/utilities/directories.py` — cross-platform path joining
- `com/vsa/metrics/HalsteadMetrics.py` — module-relative operators path + `is not ''`
- `com/vsa/multiple_files/csv_generator.py` — basename via `os.path`, drop backslash mangling

**New (create):**
- `com/vsa/gui/gui.py` — modify (image paths, `Image.LANCZOS`)
- `cli.py` — console front-end
- `desktop.py` — desktop launcher
- `samples/Original.java`, `samples/NearClone.java`, `samples/Unrelated.java`
- `tests/test_engine_smoke.py`, `tests/test_cli.py`, `tests/conftest.py`
- `Accounts/management/commands/seed_demo.py`
- `Dockerfile`, `.dockerignore`, `render.yaml`, `Makefile`, `.env.example`, `requirements-dev.txt`
- `docs/architecture.md` (diagram source), `README.md` (rewrite)

**Web (modify):** `CodeCloneDetector/settings.py`, `Accounts/templates/Accounts/login_form.html`

---

## Phase 0 — Prep

### Task 0: Branch + test tooling + ignore generated data

**Files:**
- Create: `requirements-dev.txt`
- Modify: `.gitignore`

- [ ] **Step 1: Create working branch** (repo is on `master`)

```bash
cd /Users/abdulrauf/Desktop/my-projects/code-clone-detector-new
git checkout -b fix/revive-and-showcase
```

- [ ] **Step 2: Add dev requirements**

Create `requirements-dev.txt`:

```
pytest==8.3.4
```

- [ ] **Step 3: Install pytest into the venv**

Run: `.venv/bin/python -m pip install -r requirements-dev.txt`
Expected: `Successfully installed pytest-8.3.4 ...`

- [ ] **Step 4: Ignore generated runtime data**

Append to `.gitignore`:

```
# Generated runtime data
var/
projects/
com/vsa/datasets/
staticfiles/
*.csv
```

- [ ] **Step 5: Commit**

```bash
git add requirements-dev.txt .gitignore
git commit -m "chore: add pytest and ignore generated runtime data

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Phase 1 — Engine repair (foundation)

### Task 1: Fix cosine/euclidean scalar return

**Files:**
- Modify: `com/vsa/plagiarism_techniques/cosine_distance.py`
- Modify: `com/vsa/plagiarism_techniques/euclidean_distance.py`
- Test: `tests/test_engine_smoke.py`

**Interfaces:**
- Produces: `CosineDistance().test_palgiarism(a, b) -> float` and `Euclidean_Distance().test_palgiarism(a, b) -> float`, both returning a plain Python float for 2-D single-pair inputs.

- [ ] **Step 1: Write the failing test**

Create `tests/test_engine_smoke.py`:

```python
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance


def test_cosine_returns_float_for_identical_vectors():
    result = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    assert isinstance(result, float)
    assert abs(result - 1.0) < 1e-9


def test_cosine_lower_for_dissimilar_vectors():
    same = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    diff = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[4, 3, 2, 1]])
    assert diff < same
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `.venv/bin/python -m pytest tests/test_engine_smoke.py -v`
Expected: FAIL — `TypeError: only 0-dimensional arrays can be converted to Python scalars`.

- [ ] **Step 3: Fix cosine_distance.py**

Replace the imports and `test_palgiarism` body:

```python
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class CosineDistance:

    def __init__(self):
        pass

    def test_palgiarism(self, data_set1, data_set2):
        self.data_set1 = data_set1
        self.data_set2 = data_set2
        if self.data_set1 is not None and self.data_set2 is not None:
            result = cosine_similarity(self.data_set1, self.data_set2)
            return float(np.ravel(result)[0])
```

- [ ] **Step 4: Fix euclidean_distance.py for parity**

In `test_palgiarism`, replace `return float(result)` with:

```python
            return float(np.ravel(result)[0])
```

and add `import numpy as np` near the top (after the existing scipy import).

- [ ] **Step 5: Run tests to confirm pass**

Run: `.venv/bin/python -m pytest tests/test_engine_smoke.py -v`
Expected: 2 passed.

- [ ] **Step 6: Commit**

```bash
git add tests/test_engine_smoke.py com/vsa/plagiarism_techniques/cosine_distance.py com/vsa/plagiarism_techniques/euclidean_distance.py
git commit -m "fix: extract scalar from similarity result for modern numpy

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Fix Directory cross-platform path joining

**Files:**
- Modify: `com/vsa/utilities/directories.py`
- Test: `tests/test_directories.py`

**Interfaces:**
- Produces: `Directory.get_directory_of(path) -> str` returns an existing absolute dir path ending in `os.sep`, using no literal backslashes. `Directory.path(target_dir) -> str` returns a path ending in `os.sep`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_directories.py`:

```python
import os
from com.vsa.utilities.directories import Directory


def test_get_directory_of_creates_and_ends_with_sep(tmp_path):
    target = str(tmp_path / "a" / "b")
    result = Directory.get_directory_of(target)
    assert result.endswith(os.sep)
    assert "\\" not in result or os.sep == "\\"
    assert os.path.isdir(result)


def test_path_uses_native_separator():
    result = Directory.path("datasets")
    assert "\\" not in result or os.sep == "\\"
    assert result.endswith(os.sep)
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `.venv/bin/python -m pytest tests/test_directories.py -v`
Expected: FAIL — result contains literal `\` on macOS/Linux.

- [ ] **Step 3: Fix directories.py**

Replace the `path` and `get_directory_of` methods:

```python
    @staticmethod
    def path(target_dir):
        current_dir = os.getcwd()
        if current_dir.find('gui') != -1:
            return os.path.join(current_dir.replace('gui', target_dir), '')
        return os.path.join(target_dir, '')

    @staticmethod
    def get_directory_of(path):
        path = os.path.realpath(path) + os.sep
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path
```

Also replace the two `os.path.join(os.path.realpath(dir) + "\\")` occurrences in `delete_dir` with `os.path.realpath(dir)`.

- [ ] **Step 4: Run tests to confirm pass**

Run: `.venv/bin/python -m pytest tests/test_directories.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add tests/test_directories.py com/vsa/utilities/directories.py
git commit -m "fix: use native os.sep in Directory path helpers

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Module-relative Halstead operators path + syntax warning

**Files:**
- Modify: `com/vsa/metrics/HalsteadMetrics.py`
- Test: `tests/test_engine_smoke.py` (add)

**Interfaces:**
- Consumes: the operators data file at `com/vsa/elements/operators`.
- Produces: `HalsteadMetrics().run(java_file_path)` loads operators without any absolute path.

- [ ] **Step 1: Add the failing test**

Append to `tests/test_engine_smoke.py`:

```python
def test_halstead_operators_path_is_module_relative():
    import os
    from com.vsa.metrics import HalsteadMetrics as hm_mod
    ops = os.path.join(os.path.dirname(os.path.abspath(hm_mod.__file__)),
                       '..', 'elements', 'operators')
    assert os.path.exists(ops)
```

- [ ] **Step 2: Run it (passes for existence; drives the code change)**

Run: `.venv/bin/python -m pytest tests/test_engine_smoke.py::test_halstead_operators_path_is_module_relative -v`
Expected: PASS (the file exists). This locks the path we migrate to.

- [ ] **Step 3: Fix HalsteadMetrics.py**

Ensure `import os` is present at the top. Replace the hardcoded line in `run`:

```python
        operatorsFileName = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'elements', 'operators')
```

In `readFile`, replace `if self.file_path is not '':` with:

```python
        if self.file_path != '':
```

- [ ] **Step 4: Verify no SyntaxWarning + import works**

Run: `.venv/bin/python -W error::SyntaxWarning -c "from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics; print('ok')"`
Expected: prints `ok` with no SyntaxWarning raised.

- [ ] **Step 5: Commit**

```bash
git add com/vsa/metrics/HalsteadMetrics.py tests/test_engine_smoke.py
git commit -m "fix: resolve Halstead operators file relative to module

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Fix csv_generator path handling

**Files:**
- Modify: `com/vsa/multiple_files/csv_generator.py`

**Interfaces:**
- Consumes: `Directory.get_directory_of` (Task 2), `metrics.run(path)` (n-gram/Halstead).
- Produces: `CSVGenerator.generate_multiples_csv(dir, metrics, username, project_no)` and `merge_all_csvs(path, username, project_no)` operate on native paths.

- [ ] **Step 1: Fix generate_multiples_csv path loop**

Add `import os` at the top. Replace the `for path in file_path:` loop body with:

```python
        for path in file_path:
            if len(path.strip()) > 0:
                datasets.append(metrics.run(path))
                name = os.path.basename(path).replace('.java', '.csv')
                if name.strip() != "":
                    filenames.append(name)
```

- [ ] **Step 2: Fix merge_all_csvs basename extraction**

Replace `name = [x.split('\\')[len(x.split('\\'))-1] for x in dirs]` with:

```python
        name = [os.path.basename(x) for x in dirs if x.strip()]
```

- [ ] **Step 3: Verify import still clean**

Run: `.venv/bin/python -c "from com.vsa.multiple_files.csv_generator import CSVGenerator; print('ok')"`
Expected: prints `ok`.

- [ ] **Step 4: Commit** (verified end-to-end in Task 5)

```bash
git add com/vsa/multiple_files/csv_generator.py
git commit -m "fix: use os.path.basename for cross-platform csv naming

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: End-to-end engine integration test (file-to-file + project-to-project)

This is the safety net that surfaces any remaining cross-platform/version bug in the tangled comparison path; fix whatever it reveals under approach A.

**Files:**
- Create: `samples/Original.java`, `samples/NearClone.java`, `samples/Unrelated.java`
- Test: `tests/test_engine_integration.py`
- Create: `tests/conftest.py`

**Interfaces:**
- Consumes: `Plagiarism_Tester`, `NGram_Metrics`, `CosineDistance`, `ProjectClone`.
- Produces: verified `Plagiarism_Tester(fileA, fileB).run_test(NGram_Metrics(2), CosineDistance(), is_project=False) -> float in [0,1]`.

- [ ] **Step 1: Create sample files**

`samples/Original.java`:

```java
public class Calculator {
    public int add(int a, int b) { return a + b; }
    public int sub(int a, int b) { return a - b; }
    public int mul(int a, int b) { return a * b; }
}
```

`samples/NearClone.java` (renamed identifiers, same structure):

```java
public class MathHelper {
    public int plus(int x, int y) { return x + y; }
    public int minus(int x, int y) { return x - y; }
    public int times(int x, int y) { return x * y; }
}
```

`samples/Unrelated.java`:

```java
public class Greeter {
    private String name;
    public Greeter(String n) { this.name = n; }
    public void greet() { System.out.println("Hello " + name); }
}
```

- [ ] **Step 2: Ensure repo root is importable in tests**

Create `tests/conftest.py`:

```python
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
```

- [ ] **Step 3: Write the failing integration test**

Create `tests/test_engine_integration.py`:

```python
import os

from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples")


def _compare(a, b):
    tester = Plagiarism_Tester(os.path.join(SAMPLES, a), os.path.join(SAMPLES, b))
    return tester.run_test(NGram_Metrics(2), CosineDistance(), is_project=False)


def test_file_to_file_similarity_in_range():
    score = _compare("Original.java", "NearClone.java")
    assert 0.0 <= score <= 1.0


def test_clone_scores_higher_than_unrelated():
    clone = _compare("Original.java", "NearClone.java")
    unrelated = _compare("Original.java", "Unrelated.java")
    assert clone >= unrelated
```

- [ ] **Step 4: Run it — expect failures to fix**

Run: `.venv/bin/python -m pytest tests/test_engine_integration.py -v`
Expected initially: FAIL or error. Likely culprit: `Plagiarism_Tester.make_data_for_test` writes CSVs to `Directory.path('datasets')` (a relative `datasets/` dir) that must exist. Diagnose from the traceback.

- [ ] **Step 5: Fix the write-dir creation in plagiarism_tester.py**

In `com/vsa/plagiarism_tester.py`, `make_data_for_test`, replace:

```python
        dataset_dir = Directory.path(str('datasets'))
```

with (ensures the dir exists cross-platform):

```python
        dataset_dir = Directory.get_directory_of('datasets')
```

- [ ] **Step 6: Re-run and iterate**

Run: `.venv/bin/python -m pytest tests/test_engine_integration.py -v`
Expected: both tests pass. If another path/version error surfaces, fix it in place following the same patterns (native separators, module-relative paths, scalar extraction) and note it in the commit.

- [ ] **Step 7: Commit**

```bash
git add samples/ tests/conftest.py tests/test_engine_integration.py com/vsa/plagiarism_tester.py
git commit -m "test: end-to-end engine comparison + fix dataset write dir

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Phase 2 — Console (CLI + demo)

### Task 6: CLI front-end with compare / compare-projects / demo

**Files:**
- Create: `cli.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: engine (`Plagiarism_Tester`, `NGram_Metrics`, `CosineDistance`) and `samples/`.
- Produces: `python cli.py compare A.java B.java [--ngram N]`, `python cli.py compare-projects DIR_A DIR_B [--ngram N]`, `python cli.py demo`. Exposes `compare_files(path_a, path_b, ngram=2) -> float`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_cli.py`:

```python
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_compare_files_returns_score():
    sys.path.insert(0, ROOT)
    import cli
    s = cli.compare_files(os.path.join(ROOT, "samples", "Original.java"),
                          os.path.join(ROOT, "samples", "NearClone.java"))
    assert 0.0 <= s <= 1.0


def test_demo_subcommand_runs():
    result = subprocess.run([sys.executable, "cli.py", "demo"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0
    assert "%" in result.stdout
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `.venv/bin/python -m pytest tests/test_cli.py -v`
Expected: FAIL — `No module named 'cli'`.

- [ ] **Step 3: Implement cli.py**

Create `cli.py`:

```python
#!/usr/bin/env python
"""Command-line interface for the Code Clone Detector."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance

SAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
CLONE_THRESHOLD = 0.80


def compare_files(path_a, path_b, ngram=2):
    tester = Plagiarism_Tester(path_a, path_b)
    return tester.run_test(NGram_Metrics(ngram), CosineDistance(), is_project=False)


def _verdict(score):
    return "LIKELY CLONE" if score >= CLONE_THRESHOLD else "NOT A CLONE"


def _print_result(a, b, score):
    pct = score * 100
    print(f"  {os.path.basename(a)} vs {os.path.basename(b)}")
    print(f"    similarity: {pct:.2f}%   ->  {_verdict(score)}\n")


def cmd_compare(args):
    score = compare_files(args.file_a, args.file_b, args.ngram)
    print("\nCode Clone Detector — file comparison\n")
    _print_result(args.file_a, args.file_b, score)


def cmd_compare_projects(args):
    from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
    clone = ProjectClone()
    score = clone.test_project_clone(
        file_names=['project1.csv', 'project2.csv'],
        dirs=[args.dir_a, args.dir_b],
        metrics=NGram_Metrics(args.ngram),
        tech=CosineDistance(),
        username='_cli')
    print("\nCode Clone Detector — project comparison\n")
    print(f"    similarity: {score * 100:.2f}%   ->  {_verdict(score)}\n")


def cmd_demo(args):
    print("\nCode Clone Detector — demo\n")
    print("A near-clone pair (renamed identifiers) and an unrelated pair:\n")
    _print_result(os.path.join(SAMPLES, "Original.java"),
                  os.path.join(SAMPLES, "NearClone.java"),
                  compare_files(os.path.join(SAMPLES, "Original.java"),
                                os.path.join(SAMPLES, "NearClone.java")))
    _print_result(os.path.join(SAMPLES, "Original.java"),
                  os.path.join(SAMPLES, "Unrelated.java"),
                  compare_files(os.path.join(SAMPLES, "Original.java"),
                                os.path.join(SAMPLES, "Unrelated.java")))


def build_parser():
    p = argparse.ArgumentParser(description="Detect code clones via n-grams + cosine similarity.")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("compare", help="Compare two source files.")
    c.add_argument("file_a")
    c.add_argument("file_b")
    c.add_argument("--ngram", type=int, default=2)
    c.set_defaults(func=cmd_compare)

    cp = sub.add_parser("compare-projects", help="Compare two project directories.")
    cp.add_argument("dir_a")
    cp.add_argument("dir_b")
    cp.add_argument("--ngram", type=int, default=2)
    cp.set_defaults(func=cmd_compare_projects)

    d = sub.add_parser("demo", help="Run on bundled samples.")
    d.set_defaults(func=cmd_demo)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `.venv/bin/python -m pytest tests/test_cli.py -v`
Expected: 2 passed.

- [ ] **Step 5: Eyeball the demo output**

Run: `.venv/bin/python cli.py demo`
Expected: prints two comparisons with percentages and verdicts; the near-clone pair scores higher than the unrelated pair.

- [ ] **Step 6: Commit**

```bash
git add cli.py tests/test_cli.py
git commit -m "feat: add CLI with compare, compare-projects, demo commands

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Phase 3 — Desktop (Tkinter)

### Task 7: Make the desktop app launch and run on macOS

**Files:**
- Create: `desktop.py`
- Modify: `com/vsa/gui/gui.py`
- Modify: `requirements-dev.txt` (add desktop extras) OR a new `requirements-desktop.txt`

**Interfaces:**
- Produces: `python desktop.py` opens the Tkinter GUI; logo loads; window renders without crashing on Pillow ≥10 / Python 3.12.

- [ ] **Step 1: Add desktop dependencies**

Create `requirements-desktop.txt`:

```
Pillow==11.1.0
matplotlib==3.10.0
```

Run: `.venv/bin/python -m pip install -r requirements-desktop.txt`
Expected: installs Pillow + matplotlib.

- [ ] **Step 2: Confirm Tk is available**

Run: `.venv/bin/python -c "import tkinter; tkinter.Tk().destroy(); print('tk ok')"`
Expected: `tk ok`. If it errors, document the Tk install (`brew install python-tk@3.12` or use a python.org build) in README Task 15.

- [ ] **Step 3: Fix the logo path in gui.py**

In `com/vsa/gui/gui.py`, add near the top imports:

```python
import os
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
```

Replace the hardcoded logo path (line ~69) with:

```python
        self.place_image(master=self.left_top_imgframe, path=os.path.join(IMAGES_DIR, 'logo.png'))
```

- [ ] **Step 4: Fix Pillow resampling constant**

In `place_image` (line ~109), replace `Image.ANTIALIAS` with:

```python
            canvas.image = ImageTk.PhotoImage(opImage.resize((150, 80), Image.LANCZOS))
```

Search the file for any other `Image.ANTIALIAS` and apply the same replacement.

- [ ] **Step 5: Create the launcher**

Create `desktop.py`:

```python
#!/usr/bin/env python
"""Launch the Tkinter desktop UI for the Code Clone Detector."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from com.vsa.gui.gui import GUI

if __name__ == "__main__":
    GUI()
```

- [ ] **Step 6: Launch and verify (manual — needs a display)**

Run: `.venv/bin/python desktop.py`
Expected: the "Code Cloner" window opens, the logo renders, no traceback. Close the window to exit. If a comparison button references hardcoded dataset paths (gui.py lines ~489–602), fix those to module-relative `com/vsa/datasets/...` via `Directory.get_directory_of` as encountered, matching the web flow.

- [ ] **Step 7: Commit**

```bash
git add desktop.py com/vsa/gui/gui.py requirements-desktop.txt
git commit -m "fix: launch desktop app on macOS (module-relative images, Pillow LANCZOS)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Phase 4 — Web (Django) + demo polish

### Task 8: Env-driven production settings + static serving

**Files:**
- Modify: `CodeCloneDetector/settings.py`
- Modify: `requirements.txt` (add gunicorn, whitenoise)

**Interfaces:**
- Produces: settings read `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` from env; WhiteNoise serves static; `STATIC_ROOT` set. Local defaults keep dev working.

- [ ] **Step 1: Add server deps**

Run: `.venv/bin/python -m pip install gunicorn==23.0.0 whitenoise==6.8.2`
Then regenerate the pin:
Run: `.venv/bin/python -m pip freeze > requirements.txt`
Verify `gunicorn`, `whitenoise`, `Django==4.2.*` present.

- [ ] **Step 2: Edit settings.py — env-driven core**

Replace the `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` block with:

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-only-key-set-SECRET_KEY-env-in-prod')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = [
    o for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o
]
```

- [ ] **Step 3: Add WhiteNoise middleware**

In `MIDDLEWARE`, insert directly after `SecurityMiddleware`:

```python
    'whitenoise.middleware.WhiteNoiseMiddleware',
```

- [ ] **Step 4: Add STATIC_ROOT + storage**

At the end of the static section, add:

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
```

- [ ] **Step 5: Verify check + collectstatic + dev server**

Run: `.venv/bin/python manage.py check`
Expected: no errors (staticfiles warning acceptable if `static/` empty; it exists from earlier setup).
Run: `.venv/bin/python manage.py collectstatic --noinput`
Expected: static files collected into `staticfiles/`.

- [ ] **Step 6: Commit**

```bash
git add CodeCloneDetector/settings.py requirements.txt
git commit -m "feat: env-driven settings + WhiteNoise static serving

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: seed_demo management command

**Files:**
- Create: `Accounts/management/__init__.py`
- Create: `Accounts/management/commands/__init__.py`
- Create: `Accounts/management/commands/seed_demo.py`

**Interfaces:**
- Produces: `python manage.py seed_demo` idempotently creates user `demo` (password `demo12345`) and a demo project directory seeded with sample `.java` files so a logged-in visitor can run a comparison immediately.

- [ ] **Step 1: Create package files**

Create empty `Accounts/management/__init__.py` and `Accounts/management/commands/__init__.py`.

- [ ] **Step 2: Implement seed_demo.py**

Create `Accounts/management/commands/seed_demo.py`:

```python
import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

DEMO_USER = "demo"
DEMO_PASS = "demo12345"


class Command(BaseCommand):
    help = "Create the demo user and a seeded demo project."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=DEMO_USER, defaults={"email": "demo@example.com"})
        user.set_password(DEMO_PASS)
        user.is_active = True
        user.save()
        self.stdout.write(f"demo user {'created' if created else 'updated'}: {DEMO_USER}/{DEMO_PASS}")

        samples = os.path.join(settings.BASE_DIR, "samples")
        for proj, files in (("project1", ["Original.java"]), ("project2", ["NearClone.java"])):
            dest = os.path.join(settings.BASE_DIR, "projects", DEMO_USER, proj)
            os.makedirs(dest, exist_ok=True)
            for f in files:
                src = os.path.join(samples, f)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(dest, f))
        self.stdout.write("demo project seeded under projects/demo/")
```

- [ ] **Step 3: Run it**

Run: `.venv/bin/python manage.py seed_demo`
Expected: prints `demo user created: demo/demo12345` and `demo project seeded ...`.

- [ ] **Step 4: Verify idempotency**

Run again: `.venv/bin/python manage.py seed_demo`
Expected: prints `demo user updated: demo/demo12345` (no crash, no duplicate user).

- [ ] **Step 5: Commit**

```bash
git add Accounts/management
git commit -m "feat: add seed_demo command for one-click web demo

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: Show demo credentials on login page + verify web comparison

**Files:**
- Modify: `Accounts/templates/Accounts/login_form.html`

**Interfaces:**
- Produces: login page displays the demo credentials banner when `DEMO_HINT` is enabled; the full login → compare flow returns a numeric result.

- [ ] **Step 1: Add a credentials banner to the login template**

Open `Accounts/templates/Accounts/login_form.html` and insert, immediately inside the login form container (adjust selector to match existing markup):

```html
{% if demo_hint %}
<div style="margin:1rem 0;padding:.75rem 1rem;border:1px solid #cfe;background:#eef;border-radius:6px;font-size:.9rem;">
  <strong>Demo login</strong> — username: <code>demo</code> &nbsp; password: <code>demo12345</code>
</div>
{% endif %}
```

- [ ] **Step 2: Pass the flag from the view**

In `Accounts/views.py` `login_user`, change the final render to include the flag:

```python
    import os
    return render(request, "Accounts/login_form.html",
                  {"demo_hint": os.environ.get("DEMO_HINT", "True") == "True"})
```

- [ ] **Step 3: Manual end-to-end verification**

Start the server: `.venv/bin/python manage.py runserver` (background), then in a browser: open `/accounts/login/`, confirm the banner shows; log in as `demo/demo12345`; run a comparison via the projects UI; confirm a similarity percentage renders. Stop the server.
Expected: numeric similarity result renders with no server error. If the web project-comparison path errors, fix under approach A (same path/version patterns) and note it.

- [ ] **Step 4: Commit**

```bash
git add Accounts/templates/Accounts/login_form.html Accounts/views.py
git commit -m "feat: show demo credentials on login page

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Phase 5 — Packaging (local one-command + deploy)

### Task 11: Dockerfile + .dockerignore

**Files:**
- Create: `Dockerfile`, `.dockerignore`

**Interfaces:**
- Produces: an image that installs deps, downloads nltk data, collects static, seeds demo, and serves via gunicorn on `$PORT`.

- [ ] **Step 1: Create .dockerignore**

```
.venv/
__pycache__/
*.pyc
.git/
var/
projects/
com/vsa/datasets/
staticfiles/
docs/
.idea/
```

- [ ] **Step 2: Create Dockerfile**

```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader -d /usr/local/share/nltk_data punkt punkt_tab

COPY . .

RUN python manage.py collectstatic --noinput

ENV DEBUG=False
CMD sh -c "python manage.py migrate --noinput && python manage.py seed_demo && gunicorn CodeCloneDetector.wsgi --bind 0.0.0.0:${PORT:-8000}"
```

- [ ] **Step 3: Build and run locally**

Run: `docker build -t ccd-web . && docker run --rm -e PORT=8000 -e ALLOWED_HOSTS=localhost,127.0.0.1 -p 8000:8000 ccd-web`
Expected: container starts, migrates, seeds demo, gunicorn serves. `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/` returns `200`.

- [ ] **Step 4: Commit**

```bash
git add Dockerfile .dockerignore
git commit -m "feat: containerize web app for local run and deploy

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 12: render.yaml for one-click Render deploy

**Files:**
- Create: `render.yaml`

**Interfaces:**
- Produces: a Render blueprint deploying the Dockerfile as a free web service with generated `SECRET_KEY` and correct host env.

- [ ] **Step 1: Create render.yaml**

```yaml
services:
  - type: web
    name: code-clone-detector
    runtime: docker
    plan: free
    envVars:
      - key: DEBUG
        value: "False"
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
      - key: CSRF_TRUSTED_ORIGINS
        value: "https://*.onrender.com"
      - key: DEMO_HINT
        value: "True"
```

- [ ] **Step 2: Sanity-check YAML**

Run: `.venv/bin/python -c "import yaml,sys; yaml.safe_load(open('render.yaml')); print('yaml ok')"`
(If PyYAML absent: `.venv/bin/python -m pip install pyyaml` first.)
Expected: `yaml ok`.

- [ ] **Step 3: Commit**

```bash
git add render.yaml
git commit -m "feat: add Render blueprint for free web deploy

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

- [ ] **Step 4: Deploy (manual, user-driven)**

Push the branch and open a PR (or merge), then in Render: New → Blueprint → connect the GitHub repo → apply. Record the resulting `https://<name>.onrender.com` URL for the README. Note free-tier cold start (~30–50s).

---

### Task 13: Makefile + .env.example

**Files:**
- Create: `Makefile`, `.env.example`

**Interfaces:**
- Produces: `make setup|web|cli|demo|desktop|test|docker` one-command targets.

- [ ] **Step 1: Create .env.example**

```
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=
DEMO_HINT=True
```

- [ ] **Step 2: Create Makefile** (note: recipe lines use TAB indentation)

```makefile
VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: setup web cli demo desktop test docker

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	$(PY) -m nltk.downloader -d $(VENV)/nltk_data punkt punkt_tab
	$(PY) manage.py migrate
	$(PY) manage.py seed_demo

web:
	$(PY) manage.py runserver

cli:
	$(PY) cli.py $(ARGS)

demo:
	$(PY) cli.py demo

desktop:
	$(PIP) install -r requirements-desktop.txt
	$(PY) desktop.py

test:
	$(PY) -m pytest -v

docker:
	docker build -t ccd-web . && docker run --rm -e PORT=8000 -e ALLOWED_HOSTS=localhost,127.0.0.1 -p 8000:8000 ccd-web
```

- [ ] **Step 3: Verify key targets**

Run: `make test`
Expected: full pytest suite passes.
Run: `make demo`
Expected: CLI demo prints comparisons.

- [ ] **Step 4: Commit**

```bash
git add Makefile .env.example
git commit -m "feat: add Makefile one-command targets and .env.example

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Phase 6 — Portfolio polish

### Task 14: Architecture diagram + README rewrite + media

**Files:**
- Create: `docs/architecture.md`
- Create: `docs/media/` (screenshots/GIFs)
- Modify: `README.md`

**Interfaces:**
- Produces: a portfolio-grade README with live demo link, three GIFs, an architecture diagram, how-it-works, and copy-paste run instructions.

- [ ] **Step 1: Add the architecture diagram (Mermaid)**

Create `docs/architecture.md` with a Mermaid diagram (renders on GitHub):

```markdown
# Architecture

\`\`\`mermaid
flowchart TD
    E["Shared engine (com/vsa)\nn-gram · Halstead · cosine/euclidean · CSV"]
    CLI["CLI (cli.py)"]
    D["Desktop (Tkinter, desktop.py)"]
    W["Web (Django + gunicorn)"]
    R["Render (Docker) — live demo"]
    CLI --> E
    D --> E
    W --> E
    W --> R
\`\`\`
```

- [ ] **Step 2: Capture web screenshots/GIFs**

Start the server and capture the login page (with demo banner), the projects/compare page, and a result. Save PNGs/GIF to `docs/media/`. For automated static shots, a headless capture script may be used; for GIFs, record the interaction (macOS: Cmd-Shift-5, or `ffmpeg`/Gifski). Save `docs/media/web.gif`, `docs/media/desktop.gif`, `docs/media/cli.gif` (desktop/CLI recorded from live runs).

- [ ] **Step 3: Rewrite README.md**

Replace `README.md` with sections in this order:
1. Title + one-line pitch.
2. **Live demo:** the Render URL + demo credentials (`demo` / `demo12345`) + cold-start note.
3. **Screenshots/GIFs:** embed `docs/media/web.gif`, `desktop.gif`, `cli.gif`.
4. **Architecture:** embed/link `docs/architecture.md` diagram.
5. **How it works:** n-grams + Halstead metrics + cosine/euclidean similarity (a short paragraph).
6. **Run it locally:** `make setup` then `make web` / `make demo` / `make cli ARGS="compare a.java b.java"` / `make desktop`; Tk install note for desktop.
7. **Tech stack.**
8. Credit to the original author + note that this is a revived/fixed fork.

- [ ] **Step 4: Verify README renders**

Confirm links resolve and Mermaid block is well-formed (GitHub preview). Verify media paths exist.

- [ ] **Step 5: Commit**

```bash
git add README.md docs/architecture.md docs/media
git commit -m "docs: portfolio README with live demo, diagram, and media

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Final verification (run before declaring done)

- [ ] `make test` — all engine + CLI tests pass.
- [ ] `make demo` — near-clone pair scores higher than unrelated pair.
- [ ] `make desktop` — window launches, logo renders, a comparison runs.
- [ ] `make web` — log in as `demo`, run a comparison, numeric result renders.
- [ ] `make docker` — container serves `200` at `/`.
- [ ] Render URL loads and login works (cold start allowed).
- [ ] README shows live link, three GIFs, diagram, and correct local-run commands.

## Self-Review (completed by plan author)

- **Spec coverage:** Engine repair (§4.1)→Tasks 1–5; Console (§4.2)→Tasks 5–6; Desktop (§4.3)→Task 7; Web+demo (§4.4)→Tasks 8–10; Packaging (§4.5)→Tasks 11–13; README+diagram+GIFs (§4.6)→Task 14; Testing (§5)→tests in Tasks 1–6 + Final verification. **One flagged deviation:** spec's `CCD_DATA_DIR` (§4.1) intentionally omitted (see Global Constraints scope note).
- **Placeholders:** none — every code step shows real code; "fix as encountered" steps (5.6, 7.6, 10.3) are bounded to documented patterns with the likely culprit named.
- **Type consistency:** `test_palgiarism(a,b)->float`, `compare_files(a,b,ngram=2)->float`, `Directory.get_directory_of->str (trailing os.sep)`, `seed_demo` creds `demo/demo12345`, `DEMO_HINT`/`demo_hint` flag consistent across Tasks 9–10 and render.yaml.
