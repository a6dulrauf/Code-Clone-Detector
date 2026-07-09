# Sample code to try the detector

No code of your own handy? Use these bundled samples to test all three interfaces.

## Files

| Path | What it is |
| --- | --- |
| `Original.java` | A small class |
| `NearClone.java` | `Original.java` with renamed identifiers (a clone) |
| `Unrelated.java` | Structurally different code |
| `demo-projects/project-a/` | A one-file Java "project" (`Calculator.java`) |
| `demo-projects/project-b/` | A renamed near-clone of project-a (`MathHelper.java`) |
| `demo-projects-python/project-a/` | A one-file Python "project" (`calculator.py`) |
| `demo-projects-python/project-b/` | A renamed near-clone (`math_helper.py`) |
| `python/Unrelated.py` | Structurally different Python code |

## Languages

Built-in languages: **Java, Python, C++, JavaScript, Kotlin, and C#**
(JavaScript, Kotlin and C# ship as data-driven definitions in
`com/vsa/elements/langdefs/`). Pick the language per run: CLI `--language`, the
web project's **Language** selector, or the desktop **Select Language** dropdown.
Each language has its own token vocabulary, so uploads/pickers only consider that
language's file extensions (`.java`, `.py`, `.cpp`, `.js`, `.kt`, `.cs`, ...).

**Add your own language** — no code needed:
- Drop a JSON definition in `com/vsa/elements/langdefs/` (loaded at startup), or
- Upload one at runtime from the web app's **Languages** page (paste JSON; it's
  validated and usable immediately). A ready-to-edit template is shown there.

A definition is just: `name`, `label`, `extensions`, `keywords`, `operators`, and
optional `operands` (type names). The vocabulary is `keywords + operators + operands`.

## How to test each interface

**CLI**
```bash
make demo                                                            # bundled clone vs non-clone
make cli ARGS="compare samples/Original.java samples/NearClone.java" # file vs file  -> ~100%
make cli ARGS="compare samples/Original.java samples/Unrelated.java" # file vs file  -> ~90%
make cli ARGS="compare-projects samples/demo-projects/project-a samples/demo-projects/project-b"  # -> ~98%
# Python (note --language):
make cli ARGS="compare-projects samples/demo-projects-python/project-a samples/demo-projects-python/project-b --language python"  # -> ~98%
```

**Desktop** (`make desktop`)
1. Pick a language under **Select Language** (Java by default).
2. **Browse** → select `samples/demo-projects/project-a` for Project 1.
3. **Browse** → select `samples/demo-projects/project-b` for Project 2.
4. Pick **NGram Technique** + **Cosine Distance** → **TEST PLAGIARISM**.

**Web** (`make web`, or the live demo)
- Easiest: log in as `demo` / `demo12345` → **Projects** → open the pre-seeded
  **demo-comparison** (Java) or **demo-comparison-python** project →
  **Run comparison** (no upload needed).
- Or create a project, choose its **Language**, and upload two folders of that
  language's source files as Project 1 and Project 2.

## A note on scores

The detector measures **structural** similarity. A renamed near-clone scores near
**100%**, while unrelated code scores much lower — e.g. `project-a` vs `project-b`
(clone) ≈ **100%**, `project-a` vs unrelated ≈ **30%**. The demo projects are kept
small and focused so the result is crisp.
