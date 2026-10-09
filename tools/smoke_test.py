#!/usr/bin/env python3
"""Data-free checks of small functions extracted from the original notebooks.

Only selected function definitions are compiled. Notebook setup, file I/O,
model loading, training, and evaluation cells are never executed. These checks
do not establish successful installation or reproduction of the experiments.
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd


def extract_functions(notebook: Path, name: str):
    """Yield named definitions and their one-based cell locations, not cells."""
    document = json.loads(notebook.read_text(encoding="utf-8"))
    for index, cell in enumerate(document["cells"], start=1):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell.get("source", []))
        if f"def {name}(" not in source:
            continue
        # Notebook shell commands are not Python syntax. Removing their lines
        # permits AST inspection; neither those commands nor other statements
        # in the containing cell are compiled or executed.
        python_source = "\n".join(
            "" if line.lstrip().startswith(("!", "%")) else line
            for line in source.splitlines()
        )
        tree = ast.parse(python_source, filename=str(notebook))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == name:
                # Avoid evaluating decorator/default expressions during import.
                if node.decorator_list or node.args.defaults or any(
                    value is not None for value in node.args.kw_defaults
                ):
                    raise ValueError(f"Unexpected decorated/defaulted function: {name}")
                isolated = ast.Module(body=[node], type_ignores=[])
                namespace = {"np": np, "__builtins__": {"sum": sum, "len": len}}
                exec(compile(isolated, str(notebook), "exec"), namespace)
                yield namespace[name], f"{notebook.name}:cell {index}"


class SyntheticAtom:
    def __init__(self, b_factor: float):
        self.b_factor = b_factor

    def get_bfactor(self):
        return self.b_factor


def check_average(function):
    assert function([]) is None
    np.testing.assert_allclose(
        function([SyntheticAtom(1.0), SyntheticAtom(2.0), SyntheticAtom(6.0)]), 3.0
    )
    np.testing.assert_allclose(function([SyntheticAtom(-0.5), SyntheticAtom(0.5)]), 0.0)
    return 3


def check_status(function):
    for labels, expected in [
        (["Interacting"], "Interacting"),
        (["Non-Interacting", "Interacting"], "Interacting"),
        (["Non-Interacting", "Non-Interacting"], "Non-Interacting"),
        ([], "Non-Interacting"),
    ]:
        assert function(pd.Series(labels, dtype="object")) == expected
    return 4


def check_normalization(function):
    np.testing.assert_allclose(
        function(pd.Series([1.0, 2.0, 5.0])), [0.0, 0.25, 1.0]
    )
    np.testing.assert_allclose(
        function(pd.Series([np.nan, 2.0, 6.0])), [np.nan, 0.0, 1.0], equal_nan=True
    )
    assert np.isnan(function(pd.Series([3.0, 3.0])))
    assert np.isnan(function(pd.Series([np.nan, np.nan])))
    return 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root", type=Path, default=Path(__file__).resolve().parents[1],
        help="Directory containing abdb_new_combine (default: repository root)",
    )
    args = parser.parse_args()
    notebook_root = args.source_root / "abdb_new_combine"
    evaluation = notebook_root / "step4.ipynb"
    if not evaluation.exists():
        evaluation = notebook_root / "step4"
    targets = [
        (notebook_root / "step1_part2_dataset_preparation.ipynb", "average_b_factor", 1, check_average),
        (notebook_root / "step2.ipynb", "average_b_factor", 1, check_average),
        (notebook_root / "step1_part2_dataset_preparation.ipynb", "merge_status", 1, check_status),
        (evaluation, "normalize_group", 3, check_normalization),
    ]
    count = cases = 0
    for notebook, name, expected_count, check in targets:
        definitions = list(extract_functions(notebook, name))
        if len(definitions) != expected_count:
            raise AssertionError(
                f"Expected {expected_count} {name} definition(s) in {notebook.name}; "
                f"found {len(definitions)}. Review source changes before updating this check."
            )
        for function, location in definitions:
            cases += check(function)
            count += 1
            print(f"PASS {location} {name}")
    print(f"PASS: {count} extracted functions; {cases} synthetic cases.")
    print("No research data, model weights, notebook workflow, or training was executed.")
    print("This is a limited function smoke test, not experimental reproduction.")


if __name__ == "__main__":
    main()
