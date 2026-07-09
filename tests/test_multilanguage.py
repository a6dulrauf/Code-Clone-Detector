import os
import shutil

from com.vsa.elements import languages
from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY_A = os.path.join(ROOT, "samples", "demo-projects-python", "project-a")
PY_B = os.path.join(ROOT, "samples", "demo-projects-python", "project-b")
PY_UNRELATED = os.path.join(ROOT, "samples", "python", "Unrelated.py")


def _compare(dir_a, dir_b, language, username):
    return ProjectClone().test_project_clone(
        file_names=["project1.csv", "project2.csv"],
        dirs=[dir_a, dir_b],
        metrics=NGram_Metrics(2, language=language),
        tech=CosineDistance(),
        username=username,
    )


def _write_project(base, name, filename, source):
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, filename), "w") as f:
        f.write(source)
    return d


# --- language registry -----------------------------------------------------

def test_registry_lists_expected_languages():
    # Built-ins are always present...
    assert {"java", "python", "cpp"}.issubset(set(languages.choices()))
    # ...and the bundled JSON definition is loaded data-driven.
    assert "javascript" in languages.choices()


def test_registry_resolves_aliases_and_case():
    assert languages.get("C++").name == "cpp"
    assert languages.get("PY").name == "python"
    assert languages.get("unknown-language").name == "java"  # safe default


def test_java_vocabulary_is_unchanged():
    """Backward-compat guard: the Java vocabulary must stay identical, or the
    seeded demo scores (and every existing Java comparison) would drift."""
    from com.vsa.elements.features import Features
    assert languages.get("java").vocabulary == list(Features.features)


# --- Python -----------------------------------------------------------------

def test_python_near_clone_is_detected():
    score = _compare(PY_A, PY_B, "python", "_mltest_py_clone")
    assert isinstance(score, float) and 0.0 <= score <= 1.0
    assert score >= 0.95   # renamed near-clone should read as a clone


def test_python_clone_scores_higher_than_unrelated(tmp_path):
    unrel = os.path.join(str(tmp_path), "unrel")
    os.makedirs(unrel, exist_ok=True)
    shutil.copy(PY_UNRELATED, os.path.join(unrel, "Unrelated.py"))
    clone = _compare(PY_A, PY_B, "python", "_mltest_py_c")
    unrelated = _compare(PY_A, unrel, "python", "_mltest_py_u")
    assert clone > unrelated


# --- C++ --------------------------------------------------------------------

_CPP_A = """class Calculator {
public:
    int add(int a, int b) { return a + b; }
    int sub(int a, int b) { return a - b; }
    bool positive(int v) { if (v > 0) { return true; } else { return false; } }
};
"""
# Same structure, renamed identifiers -> a near-clone.
_CPP_B = """class MathHelper {
public:
    int plus(int x, int y) { return x + y; }
    int minus(int x, int y) { return x - y; }
    bool greaterThanZero(int n) { if (n > 0) { return true; } else { return false; } }
};
"""


def test_cpp_near_clone_is_detected(tmp_path):
    a = _write_project(str(tmp_path), "project1", "calc.cpp", _CPP_A)
    b = _write_project(str(tmp_path), "project2", "helper.cpp", _CPP_B)
    score = _compare(a, b, "cpp", "_mltest_cpp")
    assert isinstance(score, float) and 0.0 <= score <= 1.0
    assert score >= 0.90   # renamed C++ near-clone


# --- data-driven / extensible languages ------------------------------------

def test_bundled_javascript_is_registered():
    assert "javascript" in languages.choices()
    assert languages.get("js").name == "javascript"          # alias resolves
    assert ".jsx" in languages.extensions("javascript")


_JS_A = """function process(a, b) {
  let total = 0;
  for (let i = 0; i < a; i = i + 1) {
    total = total + b;
  }
  if (total > 0) {
    return total;
  } else {
    return 0;
  }
}
"""
# Same structure, renamed identifiers -> near-clone.
_JS_B = """function compute(x, y) {
  let sum = 0;
  for (let k = 0; k < x; k = k + 1) {
    sum = sum + y;
  }
  if (sum > 0) {
    return sum;
  } else {
    return 0;
  }
}
"""


def test_javascript_near_clone_is_detected(tmp_path):
    a = _write_project(str(tmp_path), "project1", "a.js", _JS_A)
    b = _write_project(str(tmp_path), "project2", "b.js", _JS_B)
    score = _compare(a, b, "javascript", "_mltest_js")
    assert isinstance(score, float) and 0.0 <= score <= 1.0
    assert score >= 0.90


def test_template_is_a_valid_definition():
    assert languages.validate_definition(languages.template()) == []


def test_from_definition_derives_vocabulary_and_operators():
    d = {"name": "demo_lang", "extensions": [".dl"],
         "keywords": ["if", "else"], "operators": ["+", "="], "operands": ["Int"]}
    lang = languages.Language.from_definition(d)
    assert lang.vocabulary == ["if", "else", "Int", "+", "="]   # keywords+operands+operators
    assert lang.operators == ["+", "=", "if", "else"]           # operators+keywords (Halstead)


def test_validate_definition_rejects_bad_definitions():
    assert languages.validate_definition({}) != []                       # empty
    assert languages.validate_definition(                                 # empty extensions
        {"name": "x", "extensions": [], "keywords": ["a"], "operators": ["+"]}) != []
    errs = languages.validate_definition(                                 # built-in collision
        {"name": "java", "extensions": [".x"], "keywords": ["a"], "operators": ["+"]})
    assert any("built-in" in e for e in errs)


def test_register_definition_adds_a_usable_language():
    # Use a name that isn't already bundled so the test is self-contained.
    languages.register_definition({
        "name": "rust", "label": "Rust", "extensions": [".rs"],
        "keywords": ["fn", "let", "mut", "struct", "impl", "if", "else", "match", "for", "while", "return"],
        "operators": ["{", "}", "(", ")", "+", "-", "*", "/", "=", "==", "!=", "<", ">"],
    })
    assert "rust" in languages.choices()
    assert languages.extensions("rust") == (".rs",)
    assert languages.get("rust").vocabulary


def test_default_languages_present():
    for lang in ("java", "python", "cpp", "kotlin", "csharp", "javascript"):
        assert lang in languages.choices()
    assert languages.get("c#").name == "csharp"     # alias
    assert languages.get("kt").name == "kotlin"     # alias


_KT_A = ("class Calculator {\n  fun add(a: Int, b: Int): Int { return a + b }\n"
         "  fun sub(a: Int, b: Int): Int { return a - b }\n"
         "  fun pos(v: Int): Boolean { if (v > 0) { return true } else { return false } }\n}\n")
_KT_B = ("class MathHelper {\n  fun plus(x: Int, y: Int): Int { return x + y }\n"
         "  fun minus(x: Int, y: Int): Int { return x - y }\n"
         "  fun greater(n: Int): Boolean { if (n > 0) { return true } else { return false } }\n}\n")


def test_kotlin_near_clone_is_detected(tmp_path):
    a = _write_project(str(tmp_path), "project1", "a.kt", _KT_A)
    b = _write_project(str(tmp_path), "project2", "b.kt", _KT_B)
    assert _compare(a, b, "kotlin", "_mltest_kt") >= 0.90


_CS_A = ("public class Calculator {\n  public int Add(int a, int b) { return a + b; }\n"
         "  public int Sub(int a, int b) { return a - b; }\n"
         "  public bool Pos(int v) { if (v > 0) { return true; } else { return false; } }\n}\n")
_CS_B = ("public class MathHelper {\n  public int Plus(int x, int y) { return x + y; }\n"
         "  public int Minus(int x, int y) { return x - y; }\n"
         "  public bool Greater(int n) { if (n > 0) { return true; } else { return false; } }\n}\n")


def test_csharp_near_clone_is_detected(tmp_path):
    a = _write_project(str(tmp_path), "project1", "a.cs", _CS_A)
    b = _write_project(str(tmp_path), "project2", "b.cs", _CS_B)
    assert _compare(a, b, "csharp", "_mltest_cs") >= 0.90
