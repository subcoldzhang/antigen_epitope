#!/usr/bin/env python3
"""Read-only notebook and source hygiene checks; never execute notebook cells.

Requires nbformat and IPython. Run from any directory; the default scope is
the repository containing this script. Use --json for a machine-readable report.
"""

from __future__ import annotations

import argparse
import ast
import copy
import json
import os
from pathlib import Path
import re
import sys
import warnings


SKIP_DIRECTORIES = {"raw", "__pycache__", "node_modules", "cache", "caches"}
TEXT_SUFFIXES = {
    ".py", ".md", ".rst", ".txt", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".sh", ".bash", ".zsh", ".r", ".env",
}
MAX_TEXT_BYTES = 2 * 1024 * 1024
PRIVATE_METADATA_KEYS = {
    "colab", "widgets", "executionInfo", "outputId", "authorship_tag",
    "userId", "displayName", "user_tz", "user", "timestamp",
}
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    "aws_access_key_id": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "google_api_key": re.compile(r"\bAIza[A-Za-z0-9_-]{30,}\b"),
    "huggingface_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "openai_api_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    "credential_in_url": re.compile(r"https?://[^\s/:@]+:[^\s/@]+@"),
}
CREDENTIAL_ASSIGNMENT = re.compile(
    r"(?im)\b(?:api[_-]?key|access[_-]?token|password|passwd|client[_-]?secret|"
    r"authorization|hf_token|github_token)\b[\"']?\s*[=:]\s*"
    r"(?:[\"']([^\r\n\"']{6,})[\"']|([^\s#\"']{6,}))"
)
PLACEHOLDERS = re.compile(
    r"(?i)(?:<[^>]+>|\$\{?\w+\}?|your[_ -].*|example.*|placeholder.*|"
    r"changeme|redacted|none|null|os\.environ.*|os\.getenv.*|getenv\(.*)"
)


def issue(path, category, *, cell=None, line=None, message=None):
    result = {"path": path, "category": category}
    if cell is not None:
        result["cell"] = cell
    if line is not None:
        result["line"] = line
    if message is not None:
        result["message"] = message
    return result


def scoped_files(root):
    """Never follow links, hidden directories, or generated/raw caches."""
    for current, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories
            if not name.startswith(".") and name not in SKIP_DIRECTORIES
            and not (Path(current) / name).is_symlink()
        )
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink() or not path.is_file():
                continue
            # Resolve every candidate before reading; reject out-of-scope paths.
            if not path.resolve().is_relative_to(root):
                continue
            yield path


def metadata_has_private_fields(value):
    if isinstance(value, dict):
        return bool(PRIVATE_METADATA_KEYS.intersection(value)) or any(
            metadata_has_private_fields(item) for item in value.values()
        )
    if isinstance(value, list):
        return any(metadata_has_private_fields(item) for item in value)
    return False


def scan_secrets(text, path, *, cell=None):
    found = []
    for category, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(text):
            found.append(issue(path, category, cell=cell,
                               line=text.count("\n", 0, match.start()) + 1))
    for match in CREDENTIAL_ASSIGNMENT.finditer(text):
        candidate = match.group(1) or match.group(2)
        if PLACEHOLDERS.fullmatch(candidate.strip()):
            continue
        found.append(issue(path, "credential_assignment_candidate", cell=cell,
                           line=text.count("\n", 0, match.start()) + 1))
    return found


def check_notebook(path, relative_path, nbformat, transformer):
    problems = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return [issue(relative_path, "invalid_notebook_json")], 0
    except OSError:
        return [issue(relative_path, "notebook_read_error")], 0
    if not isinstance(payload, dict):
        return [issue(relative_path, "invalid_notebook_root")], 0
    try:
        # Use the supported validate API across nbformat versions. Older
        # versions may normalize their in-memory argument; detect and reject
        # that behavior instead of accepting a silently repaired document.
        candidate = nbformat.from_dict(copy.deepcopy(payload))
        baseline = copy.deepcopy(candidate)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nbformat.validate(candidate)
        if candidate != baseline:
            problems.append(issue(relative_path, "nbformat_validation_mutated_input"))
    except Exception as exc:
        # Validation exception strings can reproduce entire cells. Never print them.
        location = list(getattr(exc, "absolute_path", []))
        cell = location[1] + 1 if (
            len(location) > 1 and location[0] == "cells"
            and isinstance(location[1], int)
        ) else None
        problems.append(issue(relative_path, "nbformat_validation_error", cell=cell))
    if metadata_has_private_fields(payload.get("metadata", {})):
        problems.append(issue(relative_path, "private_notebook_metadata"))
    # Metadata may contain a credential even under a benign or unexpected key.
    # Reports retain only position/category, never serialized metadata values.
    for finding in scan_secrets(json.dumps(payload.get("metadata", {})), relative_path):
        finding.pop("line", None)
        finding["area"] = "notebook_metadata"
        problems.append(finding)
    cells = payload.get("cells", [])
    if not isinstance(cells, list):
        return problems + [issue(relative_path, "invalid_cells_container")], 0
    checked_code_cells = 0
    for number, cell in enumerate(cells, 1):
        if not isinstance(cell, dict):
            problems.append(issue(relative_path, "invalid_cell", cell=number))
            continue
        if cell.get("metadata", {}) != {}:
            problems.append(issue(relative_path, "cell_metadata_not_empty", cell=number))
            for finding in scan_secrets(json.dumps(cell.get("metadata", {})), relative_path, cell=number):
                finding.pop("line", None)
                finding["area"] = "cell_metadata"
                problems.append(finding)
        if cell.get("attachments"):
            problems.append(issue(relative_path, "embedded_attachment", cell=number))
        source = cell.get("source", "")
        if isinstance(source, list) and all(isinstance(line, str) for line in source):
            source = "".join(source)
        if not isinstance(source, str):
            problems.append(issue(relative_path, "invalid_cell_source", cell=number))
            continue
        problems.extend(scan_secrets(source, relative_path, cell=number))
        if cell.get("cell_type") != "code":
            continue
        checked_code_cells += 1
        if cell.get("outputs", []):
            problems.append(issue(relative_path, "saved_outputs", cell=number))
        if cell.get("execution_count") is not None:
            problems.append(issue(relative_path, "saved_execution_count", cell=number))
        try:
            transformed = transformer.transform_cell(source)
            ast.parse(transformed)
        except SyntaxError as exc:
            # Line numbers refer to transformed Python, not necessarily source lines.
            problems.append(issue(
                relative_path, "python_syntax_error", cell=number, line=exc.lineno,
                message="Syntax error after IPython transformation; line is in transformed Python.",
            ))
        except Exception:
            problems.append(issue(relative_path, "ipython_transform_error", cell=number))
    return problems, checked_code_cells


def run(root):
    try:
        import nbformat
        from IPython.core.inputtransformer2 import TransformerManager
    except ImportError:
        return {
            "status": "environment_error", "exit_code": 2,
            "issues": [issue(".", "missing_validation_dependency",
                             message="Install nbformat and IPython in the validation environment.")],
        }
    if not root.is_dir():
        return {"status": "environment_error", "exit_code": 2,
                "issues": [issue(".", "repository_directory_missing")]}
    transformer = TransformerManager()
    problems = []
    notebooks = code_cells = source_files = 0
    skipped_text = []
    self_path = Path(__file__).resolve()
    for path in scoped_files(root):
        relative = path.relative_to(root).as_posix()
        if path.resolve() == self_path:
            continue
        if path.suffix.lower() == ".ipynb":
            notebooks += 1
            found, count = check_notebook(path, relative, nbformat, transformer)
            problems.extend(found)
            code_cells += count
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name != ".env":
            continue
        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                skipped_text.append(relative)
                continue
            contents = path.read_text(encoding="utf-8")
        except UnicodeError:
            skipped_text.append(relative)
            continue
        except OSError:
            problems.append(issue(relative, "source_read_error"))
            continue
        source_files += 1
        problems.extend(scan_secrets(contents, relative))
    if not notebooks:
        problems.append(issue(".", "no_notebooks_found"))
    if skipped_text:
        problems.extend(issue(path, "source_scan_incomplete") for path in skipped_text)
    return {
        "status": "passed" if not problems else "failed",
        "exit_code": 0 if not problems else 1,
        "checks": {
            "notebooks": notebooks, "code_cells_syntax_checked": code_cells,
            "other_text_files_secret_scanned": source_files,
        },
        "issues": problems,
        "limitations": [
            "No cells, installation commands, data downloads, or model downloads were executed.",
            "Syntax success does not prove runtime correctness or experiment reproduction.",
            "Secret matching is heuristic and does not establish ownership or redistribution rights.",
            "Hidden directories, raw/cache directories, symlinks, and this scanner are excluded.",
            "Non-notebook secret scanning covers configured text extensions only.",
            "Every nonempty cell metadata object is rejected under the release hygiene policy.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Repository directory to inspect (default: this script's repository).")
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    args = parser.parse_args()
    report = run(args.root.resolve())
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Notebook/source checks:", report["status"])
        for key, count in report.get("checks", {}).items():
            print(f"  {key}: {count}")
        for item in report["issues"]:
            position = item["path"]
            if "cell" in item:
                position += f" cell {item['cell']}"
            if "line" in item:
                position += f" line {item['line']}"
            print(f"  {position}: {item['category']}")
        print("Static inspection only; no experiment was executed or reproduced.")
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
