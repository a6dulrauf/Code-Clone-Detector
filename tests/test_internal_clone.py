import os
import shutil

from com.vsa.multiple_files.csv_generator import CSVGenerator
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.projects_cloning.internal_clone.internal_clone import InternalClone
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.utilities.directories import Directory

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "samples")


def _internal_scan(src_dir, user, language="java"):
    """Generate per-file CSVs from src_dir, then run internal (within-project)
    clone detection over them — mirrors what the web 'Scan' button does."""
    csv_dir = "com/vsa/datasets/" + user + "/multiple_csv_project1"
    Directory.delete_dir(csv_dir)
    CSVGenerator.generate_multiples_csv(src_dir, NGram_Metrics(2, language=language),
                                        username=user, project_no=1)
    res = InternalClone().test_internal_clone(
        Directory.get_directory_of(csv_dir), CosineDistance(), language=language)
    Directory.delete_dir("com/vsa/datasets/" + user)
    return {k: v for k, v in res.items() if k not in ("dfs", "dfsnames")}


def test_internal_clone_finds_duplicate_file_within_a_project(tmp_path):
    """Regression: internal clone was broken on macOS/Linux (Windows-only path
    split) and returned nothing. A project with an original, its near-clone, and
    an unrelated file must yield three pairs, with the clone pair scoring highest."""
    src = os.path.join(str(tmp_path), "proj")
    os.makedirs(src)
    for f in ("Original.java", "NearClone.java", "Unrelated.java"):
        shutil.copy(os.path.join(SAMPLES, f), os.path.join(src, f))

    pairs = _internal_scan(src, "_ictest_java")

    assert len(pairs) == 3  # three files -> three unordered pairs
    clone_pair = max(pairs, key=pairs.get)
    assert "Original" in clone_pair and "NearClone" in clone_pair
    unrelated_max = max(v for k, v in pairs.items() if "Unrelated" in k)
    assert pairs[clone_pair] > unrelated_max
