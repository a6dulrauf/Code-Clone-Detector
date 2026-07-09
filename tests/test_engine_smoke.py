from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance


def test_cosine_returns_float_for_identical_vectors():
    result = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    assert isinstance(result, float)
    assert abs(result - 1.0) < 1e-9


def test_cosine_lower_for_dissimilar_vectors():
    same = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[1, 2, 3, 4]])
    diff = CosineDistance().test_palgiarism([[1, 2, 3, 4]], [[4, 3, 2, 1]])
    assert diff < same


def test_halstead_is_language_driven(tmp_path):
    """Halstead now reads its operators from the language registry (no static
    file), and its feature columns are the selected language's vocabulary."""
    from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
    from com.vsa.elements import languages

    assert HalsteadMetrics(language='java').get_features() == languages.get('java').vocabulary
    assert HalsteadMetrics(language='python').get_features() == languages.get('python').vocabulary
    # Operator sets differ per language.
    assert (HalsteadMetrics(language='python').language.operators
            != HalsteadMetrics(language='java').language.operators)

    # run() works with no external operators file.
    src = tmp_path / "a.java"
    src.write_text("public int add(int a, int b){ return a + b; }")
    operators, operands = HalsteadMetrics(language='java').run(str(src))
    assert isinstance(operators, dict) and isinstance(operands, dict)
    assert operators.get('+', 0) >= 1
