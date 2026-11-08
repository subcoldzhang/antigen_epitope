# Notebook curation

The initial code-only preparation preserved 96 source notebooks (2507 cells) for the private repository. The original Google Drive files and local source archive were retained.

Removed 2837 saved outputs, reset execution counts, and removed cell metadata and private/session notebook metadata, including Colab identifiers and stored widget state. Each notebook now has generic Python 3 kernel metadata, nbformat 4.5, and deterministic cell IDs. Existing Markdown and research code were retained.

Added the .ipynb extension to 3 extensionless step4 notebook(s). Original relative directories and other notebook filenames were preserved.

Preserved the explicitly reviewed original `abdb_v2/README.txt` byte-for-byte, including its AbDb data-source instructions and original line endings. Other text/data files are not automatically published.

## Minimal presentation and installation-syntax changes

- `YUHAO/Copy of step0_check_SI.ipynb`, cell 19: Moved exact PyMOL commands to a fenced Markdown cell; command content preserved.
- `abdb_new_combine/step4.ipynb`, cell 15: Moved exact PyMOL commands to a fenced Markdown cell; command content preserved.
- `abdb_new_method/step4.ipynb`, cell 53: Moved exact PyMOL commands to a fenced Markdown cell; command content preserved.
- `abdb_v4/step4_CNN_predict_B_factor_SasaRate_cutoff.ipynb`, cell 4: Prefixed the exact bare ipywidgets installation line with the IPython % magic.
- `abdb_v4/step4_CNN_predict_B_factor_SasaRate_cutoff.ipynb`, cell 60: Moved exact PyMOL commands to a fenced Markdown cell; command content preserved.

Matching was by exact whole-cell source, not a keyword replacement. PyMOL commands remain verbatim inside their code fence. No scientific parameter, model architecture, algorithm, threshold, data-selection rule, or metric calculation was changed.

## Integrity and limits

`SOURCE_MANIFEST.json` records original/published paths, original-file and published-file SHA-256 values, aggregate and per-cell source checksums, and every allowed source-cell change. Source checksums use UTF-8 text; aggregate checksums use canonical JSON of ordered `cell_type`/`source` pairs. It also lists removed metadata field names without private values and preserves only selected nonprivate runtime/hardware hints. Its `source_documents` section records paths, byte counts and original/published hashes for 1 explicitly approved provenance document(s).

Notebook schema validation passed for each prepared artifact. This curation process does not execute the notebooks or establish installation, scientific correctness, or experimental reproduction. Existing runtime/research issues remain documented separately.

The preparation tool refuses nonempty attachments, unreviewed metadata keys, or unknown notebook/cell extension fields rather than silently dropping potentially meaningful content. No such unreviewed content was discarded in this release.

Datasets, model weights, generated scientific results, environment directories, and local curation tools were excluded from the initial code-only release.

## Core-data update — 2026-11-08

The [core-data Release](https://github.com/subcoldzhang/antigen_epitope/releases/tag/data-core-2026-11-08) adds one archive, `core-experiment-inputs.tar.gz`, while keeping data payloads out of Git history. It contains 1,261 existing files totaling 1,205,977,471 uncompressed bytes and 277,243,644 compressed bytes: 1,151 PDB files under `abdb_v3/pdb/`, 36 non-OBJ files under `abdb_new_combine/data/`, and 74 direct text/CSV inputs from the five `abdb_v4` folds. Historical SAbDab PDB/TSV/CSV files under the root `data/` directory, the approximately 80 GB mesh collection, NPY tensors, trained weights, and generated results are excluded from this update.

[DATA.md](DATA.md) records acquisition and extraction instructions, [DATA_FILES.tsv](DATA_FILES.tsv) records per-file SHA-256 values for the 1,261 included files, and [DATA_FOLD_MEMBERSHIP.tsv](DATA_FOLD_MEMBERSHIP.tsv) records 4,834 preserved fold-directory memberships. These data manifests supplement the original notebook source manifest; they do not change its historical curation record.

The source `abdb_v4/fold_2/data/` directory is empty and the required training CSV is missing. No replacement training data, fold allocation, or scientific output was generated to fill these gaps. File packaging and integrity checks do not establish experimental reproduction; the source and validation limitations above still apply.
