#!/usr/bin/env python
"""Command-line interface for the Code Clone Detector."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance

SAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
# Structural n-gram similarity runs high for same-language code; true near-
# duplicates score ~0.98-1.0 while merely-similar code sits below ~0.92.
CLONE_THRESHOLD = 0.95


def compare_files(path_a, path_b, ngram=2):
    tester = Plagiarism_Tester(path_a, path_b)
    return tester.run_test(NGram_Metrics(ngram), CosineDistance(), is_project=False)


def _verdict(score):
    return "LIKELY CLONE" if score >= CLONE_THRESHOLD else "NOT A CLONE"


def _print_result(a, b, score):
    pct = score * 100
    print(f"  {os.path.basename(a)} vs {os.path.basename(b)}")
    print(f"    similarity: {pct:.2f}%   ->  {_verdict(score)}\n")


def cmd_compare(args):
    score = compare_files(args.file_a, args.file_b, args.ngram)
    print("\nCode Clone Detector — file comparison\n")
    _print_result(args.file_a, args.file_b, score)


def cmd_compare_projects(args):
    from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
    clone = ProjectClone()
    score = clone.test_project_clone(
        file_names=['project1.csv', 'project2.csv'],
        dirs=[args.dir_a, args.dir_b],
        metrics=NGram_Metrics(args.ngram),
        tech=CosineDistance(),
        username='_cli')
    print("\nCode Clone Detector — project comparison\n")
    print(f"    similarity: {score * 100:.2f}%   ->  {_verdict(score)}\n")


def cmd_demo(args):
    print("\nCode Clone Detector — demo\n")
    print("A near-clone pair (renamed identifiers) and an unrelated pair:\n")
    _print_result(os.path.join(SAMPLES, "Original.java"),
                  os.path.join(SAMPLES, "NearClone.java"),
                  compare_files(os.path.join(SAMPLES, "Original.java"),
                                os.path.join(SAMPLES, "NearClone.java")))
    _print_result(os.path.join(SAMPLES, "Original.java"),
                  os.path.join(SAMPLES, "Unrelated.java"),
                  compare_files(os.path.join(SAMPLES, "Original.java"),
                                os.path.join(SAMPLES, "Unrelated.java")))


def build_parser():
    p = argparse.ArgumentParser(description="Detect code clones via n-grams + cosine similarity.")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("compare", help="Compare two source files.")
    c.add_argument("file_a")
    c.add_argument("file_b")
    c.add_argument("--ngram", type=int, default=2)
    c.set_defaults(func=cmd_compare)

    cp = sub.add_parser("compare-projects", help="Compare two project directories.")
    cp.add_argument("dir_a")
    cp.add_argument("dir_b")
    cp.add_argument("--ngram", type=int, default=2)
    cp.set_defaults(func=cmd_compare_projects)

    d = sub.add_parser("demo", help="Run on bundled samples.")
    d.set_defaults(func=cmd_demo)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
