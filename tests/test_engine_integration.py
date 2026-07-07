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
