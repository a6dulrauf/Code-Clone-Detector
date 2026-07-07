import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_compare_files_returns_score():
    sys.path.insert(0, ROOT)
    import cli
    s = cli.compare_files(os.path.join(ROOT, "samples", "Original.java"),
                          os.path.join(ROOT, "samples", "NearClone.java"))
    assert 0.0 <= s <= 1.0


def test_demo_subcommand_runs():
    result = subprocess.run([sys.executable, "cli.py", "demo"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0
    assert "%" in result.stdout
