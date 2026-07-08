import os
import shutil

from CodeClone.view_models import ProjectViewModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "samples")


def _make_project(base, name, src_files):
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    for f in src_files:
        shutil.copy(os.path.join(SAMPLES, f), os.path.join(d, f))
    return d


def test_web_project_comparison_returns_score(tmp_path):
    p1 = _make_project(str(tmp_path), "project1", ["Original.java"])
    p2 = _make_project(str(tmp_path), "project2", ["NearClone.java"])
    score = ProjectViewModel().run_test_Project("_webtest", dirs=[p1, p2], ngram=2)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0
