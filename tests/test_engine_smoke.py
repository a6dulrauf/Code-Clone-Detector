from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance


def test_cosine_returns_float_for_identical_vectors():
    result = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    assert isinstance(result, float)
    assert abs(result - 1.0) < 1e-9


def test_cosine_lower_for_dissimilar_vectors():
    same = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    diff = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[4, 3, 2, 1]])
    assert diff < same
