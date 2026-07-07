from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance


def test_cosine_returns_float_for_identical_vectors():
    result = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    assert isinstance(result, float)
    assert abs(result - 1.0) < 1e-9


def test_cosine_lower_for_dissimilar_vectors():
    same = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    diff = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[4, 3, 2, 1]])
    assert diff < same


def test_halstead_operators_path_is_module_relative():
    import os
    from com.vsa.metrics import HalsteadMetrics as hm_mod
    ops = os.path.join(os.path.dirname(os.path.abspath(hm_mod.__file__)),
                       '..', 'elements', 'operators')
    assert os.path.exists(ops)
