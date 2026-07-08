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
