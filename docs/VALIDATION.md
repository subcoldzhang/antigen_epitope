# Validation record

Repository preparation was checked on 2026-10-09 using Python 3.14.4 on macOS
arm64. This record distinguishes code-publication checks from scientific runs.

## Lightweight environment

The direct dependencies in `requirements-validation.txt` were installed from
official PyPI into a new virtual environment. The resulting versions were saved
in `requirements-validation.lock.txt`. That lock file was then installed into a
second, empty virtual environment; installation and `python -m pip check` passed
in both environments. No research data or model weights were required.

The environment contains the packages needed for notebook inspection and the
synthetic function checks. It is not the original Colab environment and does not
validate the candidate scientific dependency files.

## Notebook publication checks

The final publication tree contains 96 notebooks with 2,507 cells. Running
`python tools/check_notebooks.py --json` passed notebook-schema checks, syntax
checks for 2,454 code cells after IPython transformation, output/metadata hygiene
checks, and heuristic credential checks, with zero reported issues. The checker
also scanned 13 other text files. It did not execute research cells.

The curation process removed 2,837 stored output objects, cleared execution
counts, and removed personal/session metadata. Three extensionless notebooks
received the `.ipynb` extension. Four cells containing standalone PyMOL commands
were retained as fenced Markdown instructions, and one bare installation line
was changed to the IPython `%pip` form. Scientific parameters and algorithms were
not changed. Details and per-file/per-cell checksums are recorded in
[CURATION.md](CURATION.md) and [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).

## Synthetic function checks

`python tools/smoke_test.py` checks six function definitions extracted from the
preserved `abdb_new_combine` notebooks: two residue B-factor averaging functions,
one interaction-status aggregation function, and three score-normalization
functions. All 22 synthetic cases passed against the retained original source
in both environments. The same 22 cases also passed against the final publication
copies in the primary validation environment, followed by a passing `pip check`.

Only the selected function definitions are compiled and called. The checks do
not execute notebook setup cells, mount Drive, read a research dataset, invoke a
pretrained model loader, train a model, or evaluate biological predictions.

## Research execution not performed

The following remain unverified:

- Installation and compatibility of the scientific dependency layers, including
  PyMOL, PyMesh, geometry libraries, TensorFlow, PyTorch, and ESM runtimes.
- Real-data preprocessing, contact labels, shape-index generation, and embedding
  inference.
- Training, fold construction, model loading, prediction, and evaluation.
- Reproduction of any result in a manuscript.

Training data, model weights, prepared features, and generated scientific results
were deliberately excluded from acquisition for execution and from publication.
Historical notebook outputs were removed from the publication copies; those
outputs are not evidence of a fresh reproduction run. See
[REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the missing inputs, environment
constraints, and scientific decisions that must be resolved before such a run.

The publication checks are limited in scope. Valid notebook syntax does not
establish runtime correctness; synthetic function tests do not establish
scientific validity; heuristic credential checks do not guarantee that all
possible secrets have been detected.
