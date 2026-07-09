import os
import shutil

from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "samples")


def _project(base, name, files):
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    for f in files:
        shutil.copy(os.path.join(SAMPLES, f), os.path.join(d, f))
    return d


def _compare(base, files_a, files_b, username):
    a = _project(base, "project1", files_a)
    b = _project(base, "project2", files_b)
    return ProjectClone().test_project_clone(
        file_names=["project1.csv", "project2.csv"],
        dirs=[a, b],
        metrics=NGram_Metrics(2),
        tech=CosineDistance(),
        username=username,
    )


def test_project_comparison_returns_score(tmp_path):
    score = _compare(str(tmp_path), ["Original.java"], ["NearClone.java"], "_projtest_clone")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_project_clone_scores_at_least_as_high_as_unrelated(tmp_path):
    clone = _compare(str(tmp_path / "a"), ["Original.java"], ["NearClone.java"], "_projtest_a")
    unrelated = _compare(str(tmp_path / "b"), ["Original.java"], ["Unrelated.java"], "_projtest_b")
    assert clone >= unrelated


def test_repeated_comparisons_do_not_accumulate(tmp_path):
    """Regression: consecutive comparisons under the SAME username must clean
    their dataset dirs first. Otherwise stale per-file CSVs are re-merged, the
    two projects get mismatched feature dimensions, and cosine similarity
    raises 'Incompatible dimension'. This is what broke the desktop app."""
    user = "_projtest_repeat"
    clone1 = _compare(str(tmp_path / "r1"), ["Original.java"], ["NearClone.java"], user)
    # Same username, a DIFFERENT second project — used to crash via accumulation.
    unrelated = _compare(str(tmp_path / "r2"), ["Original.java"], ["Unrelated.java"], user)
    clone2 = _compare(str(tmp_path / "r3"), ["Original.java"], ["NearClone.java"], user)
    assert all(0.0 <= s <= 1.0 for s in (clone1, unrelated, clone2))
    assert abs(clone1 - clone2) < 1e-9   # deterministic across runs (no leakage)
    assert clone1 > unrelated            # still discriminates
