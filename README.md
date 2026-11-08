# antigen_epitope

Research notebooks for antigen residue features, antibody-contact labels, protein embeddings, and epitope-classification experiments. The collection includes structural preprocessing with Biopython/PyMOL, alternative surface shape-index calculations, ESM embedding experiments, and neural-network training and evaluation.

This private repository is being prepared as a companion to a research paper. It preserves research variants and their parameter choices; the author-approved manuscript workflow has not yet been identified. **End-to-end reproduction has not been verified.** Paper details, citation, and license remain to be confirmed.

## Repository guide

| Location | Purpose |
| --- | --- |
| Root `step1_*.ipynb` notebooks | Alternative structure preparation, residue features, contact definitions, and shape-index experiments. |
| `step2_colab.ipynb` | Another structural feature-preparation variant; it is not a training entry point. |
| `secondary_structure.ipynb` | Exploratory secondary-structure inspection and PDB visualization examples. |
| `abdb_new_combine/` | SI-table preparation, ESM2 embeddings, an incomplete ESM3 alternative, classifier training, and evaluation. |
| `abdb/`, `abdb_v2/`–`abdb_v5/`, `abdb_combine/`, `abdb_new_method/`, `sabdab/`, `YUHAO/`, and notebook-bearing subdirectories under `data/` | Preserved historical variants and supporting code; directory names alone do not identify the manuscript's final version. Core data are distributed separately as Release assets; see [docs/DATA.md](docs/DATA.md). |
| `tools/check_notebooks.py` | Notebook schema, transformed Python syntax, output/metadata hygiene, and heuristic credential checks without executing cells. |
| `tools/smoke_test.py` | Data-free synthetic checks of selected functions extracted from `abdb_new_combine` notebooks. |
| `requirements-validation*.txt` | Dependencies for repository checks only. |
| `requirements.txt`, `requirements-ml.txt`, `requirements-geometry.txt` | Source-derived candidate research dependency layers; installation and research compatibility remain unverified. |
| [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) | Input/output contracts, environment constraints, execution choices, and unresolved reproduction requirements. |
| [docs/PARAMETERS.md](docs/PARAMETERS.md) | Read-only index of important embedded parameters, with notebook paths and original cell numbers. |
| [docs/VALIDATION.md](docs/VALIDATION.md) | Recorded checks, their exact scope, and remaining verification limits. |
| [docs/CURATION.md](docs/CURATION.md) | Publication cleanup, exclusions, and source-preservation decisions. |
| [docs/SOURCE_MANIFEST.json](docs/SOURCE_MANIFEST.json) | Source inventory and provenance mapping. |
| [docs/DATA.md](docs/DATA.md) | Core-data Release downloads, scope, file checksums, fold membership, and known gaps. |

Research data are distributed through GitHub Releases rather than stored in Git history. Notebook outputs, package caches, mesh files, NPY tensors, model weights, and generated results remain excluded from this core-data snapshot. Parameter values remain in the research source; a complete training package and trained predictor are not supplied.

**Data update — 2026-11-08:** The [core-data Release](https://github.com/subcoldzhang/antigen_epitope/releases/tag/data-core-2026-11-08) provides one archive, `core-experiment-inputs.tar.gz`: **1,261 files, 1,205,977,471 uncompressed bytes, and 277,243,644 compressed bytes**. It contains 1,151 PDB files under `abdb_v3/pdb/`, 36 existing non-OBJ files under `abdb_new_combine/data/`, and 74 direct text/CSV inputs from the five `abdb_v4` folds. Historical SAbDab PDB/TSV/CSV files under the root `data/` directory and the approximately 80 GB mesh collection are outside this release. See [the data guide](docs/DATA.md), [per-file SHA-256 manifest](docs/DATA_FILES.tsv), and [fold-membership manifest](docs/DATA_FOLD_MEMBERSHIP.tsv). The source `abdb_v4/fold_2/data/` directory is empty and the required training CSV is missing; these gaps have not been filled by reconstructed data. Uploading the existing files does not establish end-to-end reproduction.

## Start with the data-free checks

Clone the private repository using a GitHub account with access:

```sh
git clone https://github.com/subcoldzhang/antigen_epitope.git
cd antigen_epitope
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validation.lock.txt
python -m pip check
python tools/check_notebooks.py
python tools/smoke_test.py
```

The pinned validation environment was installed and checked on **Python 3.14.4, macOS arm64**. `pip check` passed, and the synthetic smoke test passed **22 cases across 6 extracted function definitions**. The lock file records that lightweight environment; it is not a historical experiment lock or a cross-platform guarantee. `requirements-validation.txt` lists its direct dependencies if a fresh platform-specific resolution is needed.

The notebook checker reads source and validates syntax after IPython transformation; it does not run installation commands or notebook cells. The smoke test exercises B-factor averaging, status aggregation, and score normalization with synthetic values. Neither command downloads research data or model weights, mounts Drive, trains a model, or establishes biological accuracy.

## Prepare a research environment

Choose the intended notebook and scientific branch before installing the heavier dependencies. The notebooks contain historical Colab setup cells rather than one verified project-wide environment.

The source-derived requirement layers provide **candidate installation commands, not tested research installation instructions**. First select a compatible Python/runtime and activate a separate scientific environment; the Python 3.14 validation environment above is not a recommendation for PyMesh, TensorFlow, or the ESM workflows. Install the layer needed for the selected notebook:

```sh
# Base analysis and Jupyter tools:
python -m pip install -r requirements.txt

# Alternative: base plus ESM2 / classifier dependencies:
python -m pip install -r requirements-ml.txt

# Alternative: base plus geometry / visualization dependencies:
python -m pip install -r requirements-geometry.txt
```

The ML and geometry files each include the base file. These three installations were **not executed or tested** during repository preparation. PyMOL and the specific PyMesh binary require separate platform-appropriate setup and are intentionally absent from these pip lists. ESM3 is also omitted from the ESM2 dependency layer; its incomplete branch needs a separate environment. Native libraries, GPU support, version conflicts, and model access still require validation.

| Workflow | Requirements visible in source | Status |
| --- | --- | --- |
| Structure and residue features | NumPy, pandas, Biopython, SciPy, PyMOL | Real-data execution unverified. |
| Surface geometry | Variant-dependent PyMesh, PyVista, PyWavefront, trimesh, rtree, and notebook visualization libraries | Platform-specific setup unverified. |
| ESM2 embeddings | PyTorch and `fair-esm`; externally obtained ESM2 weights | Weight loading/inference unverified. |
| Classifiers | TensorFlow/Keras for the reviewed dense branch; PyTorch/torchvision/torchsummary for historical CNN variants; scikit-learn and plotting dependencies | Training/evaluation unverified. |
| ESM3 alternative | Separate ESM SDK, compatible PyTorch/CUDA environment, approved model access | Incomplete source; not a runnable pipeline. |

The historical PyMesh wheel named in the notebooks targets **CPython 3.10 / Linux x86_64**, unlike the validation environment above. PyMOL installation cells use Linux `apt-get`. ESM2's `fair-esm` and the ESM3 SDK both use the `esm` import namespace and should be configured in separate research environments. See the detailed [environment notes](docs/REPRODUCIBILITY.md#environment-boundaries).

## Prepare external data and select a workflow

Download and verify `core-experiment-inputs.tar.gz` using [docs/DATA.md](docs/DATA.md), then extract it into a working directory outside the Git checkout. Edit path assignments in a working copy of the selected notebook to point there; the preserved notebooks do not automatically read environment variables or a configuration file.

Data sources differ by research version. The root preprocessing notebooks reference SAbDab metadata and corresponding PDB structures; their legacy source URL now redirects to the [SAbDab2 search page](https://sabdab.opig.stats.ox.ac.uk/search/?all=true). The exact historical snapshot is unknown. Separately, the original [abdb_v2/README.txt](abdb_v2/README.txt) identifies [AbDb](http://www.abybank.org/abdb/) and the selection note **“Kabat ==> NR”** as the PDB source for that version. The AbDb link timed out during preparation, so its present download availability was not verified. Neither reference identifies a complete versioned reproduction dataset.

The private core-data Release supplies the existing files listed in its manifests, including prepared tables and selected fold inputs. Confirm which files belong to the selected manuscript workflow, retain their checksums, and obtain any missing inputs and matching classifier weights separately. The snapshot does not establish the original acquisition dates, completeness, or scientific validity of the fold construction.

Two useful places to inspect are:

1. **Structural preprocessing:** `step1_colab_zhaoqian.ipynb` extracts residue features/contact labels. `step1_colab_xiaohan_add_SI.ipynb` additionally exports residue shape-index tables. Choose one contact definition and one SI method; their alternatives are not interchangeable.
2. **Embeddings and classifier experiments:** `abdb_new_combine/step2.ipynb` contains the ESM2 feature path. `step3.ipynb` trains a dense classifier from prepared patch embeddings, but reads inputs from sibling project directories. `step4.ipynb` contains alternative evaluation blocks. These filenames do not form a self-contained linear pipeline.

After preparing a separate Jupyter research environment and external inputs, open a selected notebook, for example:

```sh
jupyter lab step1_colab_zhaoqian.ipynb
# Or inspect the separate ESM2 workflow:
jupyter lab abdb_new_combine/step2.ipynb
```

JupyterLab and the research dependencies are not installed by the validation requirements. In Colab, review the original Drive-mount and installation cells for the chosen runtime. **Do not use “Run all” as a reproduction command:** notebooks contain alternative branches, repeated writes, data/model downloads, and—in some variants—directory deletion. Follow the [stage-by-stage guide](docs/REPRODUCIBILITY.md#reviewed-workflows), supply missing inputs, and execute only the intended cells in an independent working copy.

Structural preparation produces selected-complex/antigen PDB files, surface meshes, and residue TSVs containing coordinates, secondary structure, relative SASA, contact indicators, and optional SI. The reviewed ESM2 path adds 320 embedding columns; the classifier path consumes prepared residue patches and writes a Keras `.h5` model. Evaluation prints metrics/plots and can export prediction-colored PDBs. Some existing structures and prepared tables are preserved in the core-data Release; meshes, weights, and generated evaluation results are outside its scope. New outputs should remain in the external working directory.

## Reproduction status and publication checklist

Lightweight installation, dependency consistency, and the synthetic function examples have passed. Full structural preprocessing, geometry, pretrained embedding inference, training, prediction, and manuscript-result reproduction have not been run for this release.

See [the validation record](docs/VALIDATION.md) for the completed checks and their limits, and [curation notes](docs/CURATION.md) for narrowly scoped notebook compatibility edits. A schema/syntax pass does not establish that the notebook can run with real inputs.

Before a public paper release, confirm:

- The canonical source revision, notebook variants, contact/SI definitions, and selected evaluation blocks.
- The paper title, authors, DOI or other identifier, and citation text.
- The repository license and resource provenance/redistribution permissions.
- Versioned external datasets, fold/patch definitions, weights, and retrieval instructions.
- A tested research environment, hardware requirements, random seeds, and an independently checked train/test protocol.
- Fresh end-to-end execution records and the relationship between generated outputs and reported paper results.

No license or paper citation has been invented for this preparation snapshot.
