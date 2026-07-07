import os
from com.vsa.utilities.directories import Directory


def test_get_directory_of_creates_and_ends_with_sep(tmp_path):
    target = str(tmp_path / "a" / "b")
    result = Directory.get_directory_of(target)
    assert result.endswith(os.sep)
    assert "\\" not in result or os.sep == "\\"
    assert os.path.isdir(result)


def test_path_uses_native_separator():
    result = Directory.path("datasets")
    assert "\\" not in result or os.sep == "\\"
    assert result.endswith(os.sep)
