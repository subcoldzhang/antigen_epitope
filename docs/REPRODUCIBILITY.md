# Reproducibility guide

This guide documents the source behavior reviewed during repository preparation on 2026-10-09. It covers the root structural notebooks and `abdb_new_combine` in detail. Other preserved research variants need their own manuscript-version mapping. Inclusion in the repository does not establish that a notebook generated a reported paper result.

Use [PARAMETERS.md](PARAMETERS.md) to locate embedded research settings, [CURATION.md](CURATION.md) for packaging decisions, [VALIDATION.md](VALIDATION.md) for the recorded checks, and [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) for source provenance. The parameter index is documentation only; it is not a shared configuration or a selection of manuscript defaults.

The release contains code, parameter choices, and documentation. Research inputs, model weights, notebook outputs, and generated scientific products are intentionally absent. No training dataset, pretrained model, or scientific result was downloaded or regenerated as part of the lightweight verification described below.

## Verified scope

| Check | Outcome and limit |
| --- | --- |
| Isolated validation dependency installation | Passed on Python 3.14.4 / macOS arm64 using the validation requirements. This does not install the research environment. |
| Dependency consistency | `python -m pip check` passed in that environment. |
| Synthetic function smoke test | 6 extracted definitions / 22 cases passed: two B-factor averaging functions, one status aggregation function, and three normalization functions. No complete notebook cell was executed. |
| Notebook inspection | Source was reviewed for inputs, writes, dependencies, parameters, and alternative branches. `tools/check_notebooks.py` provides repeatable schema, syntax, and hygiene checks on the release tree. |
| Real structure processing, PyMOL/PyMesh geometry, ESM inference | Not verified. External resources and compatible research environments were not supplied for execution. |
| Training, model loading, evaluation, manuscript reproduction | Not verified. No experiment-success or metric claim is made. |

The lightweight commands are:

```sh
python -m pip install -r requirements-validation.lock.txt
python -m pip check
python tools/check_notebooks.py
python tools/smoke_test.py
```

Run these in a dedicated virtual environment as described in the README. Syntax checking cannot detect missing variables, absent input data, incompatible compiled libraries, incorrect row alignment, or scientific protocol problems. Credential matching is heuristic and does not establish data ownership or redistribution rights.

## Environment boundaries

The repository has no verified universal research environment. Preserve the distinction between the working validation environment and the historical research setup:

- **Validation:** NumPy, pandas, nbformat, and IPython, with resolved versions in `requirements-validation.lock.txt`. No structural or machine-learning libraries are required for these checks.
- **Structural features:** Biopython, NumPy, pandas, SciPy, and PyMOL. Source setup uses `apt-get install -y python3-pymol`; the interpreter running the notebook must be able to import that installation. Colab-specific `google.colab` imports do not work in an ordinary local Jupyter kernel.
- **Mesh experiments:** Dependencies differ by notebook. The historical file `pymesh2-0.3.1-cp310-cp310-linux_x86_64.whl` is a Python 3.10/Linux x86_64 binary. It does not install into the macOS arm64 validation environment. The source references the [PyMesh binary releases](https://github.com/nuvolos-cloud/PyMesh/releases). Exact compatibility still needs testing. PyVista, PyWavefront, trimesh, rtree, ipyvolume, matplotlib, and ipywidgets appear in different variants; Yuhao's installation cells also request open3d and `pyglet<2`.
- **ESM2:** `torch` plus `fair-esm`, whose import name is `esm`. The reviewed branch uses `esm2_t6_8M_UR50D`, representation layer 6, and 320 embedding values per residue. It does not explicitly move the model to CUDA. See [FAIR ESM usage](https://github.com/facebookresearch/esm#usage).
- **Classifiers:** The reviewed `abdb_new_combine` dense branch uses TensorFlow/Keras, scikit-learn, NumPy, pandas, and matplotlib. Historical CNN variants use PyTorch, torchvision, and torchsummary; evaluation notebooks also import torchvision and tqdm. Exact historical versions have not been established.
- **ESM3:** The separate [ESM SDK](https://github.com/Biohub/esm), model access, and a compatible CUDA runtime are assumed by the incomplete alternative. Use a separate environment from `fair-esm`; the overlapping `esm` namespace must not be resolved by blindly installing both distributions together.

Stored installation output in the original `abdb_new_combine` files mentions fair-esm 2.0.0, Biopython 1.85, NumPy 2.0.2, and a Python 3.11 path. These observations are incomplete historical evidence, not a tested lock file. Current unpinned installations cannot establish the historical environment. The root PyMesh binary and the later Colab outputs also point to different Python versions.

### Candidate research installations — untested

The following files were assembled from imports and installation statements across the research source. They do not pin a historical environment and their installation/resolution was not exercised:

| File | Coverage | Deliberate omissions / limits |
| --- | --- | --- |
| `requirements.txt` | NumPy, pandas, SciPy, Biopython, scikit-learn, matplotlib, seaborn, tqdm, Jupyter/IPython/nbformat, and ipywidgets. | Does not supply Colab, PyMOL, PyMesh, machine-learning runtimes, or model weights. |
| `requirements-ml.txt` | Includes the base file, then torch, torchvision, torchsummary, TensorFlow, and fair-esm. | Not GPU-tested or installation-tested. ESM3 and huggingface-hub are excluded because their separate SDK environment is unresolved. |
| `requirements-geometry.txt` | Includes the base file, then PyWavefront, ipyvolume, PyVista, trimesh, rtree, FreeSASA, Open3D, `pyglet<2`, and ProDy. | PyMOL and the specific PyMesh wheel are excluded. Native dependencies/rendering remain unverified. ProDy appears in an exploratory installation cell without a direct import. |

After choosing a compatible scientific interpreter and activating a separate environment, a candidate installation is one of:

```sh
python -m pip install -r requirements.txt
# Or, for a selected ESM2 / classifier workflow:
python -m pip install -r requirements-ml.txt
# Or, for a selected geometry workflow:
python -m pip install -r requirements-geometry.txt
```

These are examples for future environment validation, not commands reported as successful in this release. Do not infer scientific compatibility from the Python 3.14.4 validation lock. Resolve platform-specific PyMOL/PyMesh requirements separately; confirm native-library compatibility for FreeSASA, Rtree, Open3D, and rendering. A workflow using both ML and geometry still needs an explicitly resolved environment rather than assuming the two unpinned layers are compatible. After a successful future installation, record `pip check`, actual import/ABI checks, and the resolved environment before attempting data processing.

## External inputs and paths

Choose a separate working tree for data and generated products. The following is a **placement template**, not a bundled dataset or an automatically consumed configuration:

```text
<external-workspace>/
  data/
    sabdab_protein_summary.tsv
    structures/
    antigen_pdbs/
    antigen_objs/
    antigen_info/
    antigen_info_SI/
  abdb_new_combine/
    data/
      antigen_pdb_with_SI/
      antigen_pdbs/
      antigen_info/
      antigen_info_SI/
      antigen_info_SI_interaction/
      all_antigen_info_SI/
      all_data_with_SI.csv
    results/
  abdb_v4/
    fold_<1..5>/
      data_processed_step1_with_SI/
  abdb_new_method/
    fold_<1..5>/
      data/
        all_data_with_SI.csv
      data_processed_step1_with_SI/
```

Not every stage uses every directory, and additional research variants have their own paths. Review the exact selected cells before creating or populating directories. Keep this working tree outside Git; the notebooks do not read the `<external-workspace>` placeholder automatically.

### Path conventions that need reconciliation

- Most root notebooks use `/content/drive/MyDrive/@antibody/antigen_epitope/`.
- `step1_part1_mesh_SI_calculation_yuhao.ipynb` uses `/content/drive/MyDrive/antigen_epitope/`, then changes its mesh input assignments to a `YUHAO/data/` subtree.
- `abdb_new_combine` uses `/content/drive/MyDrive/@antigen_epitope/` and reads several inputs from sibling `abdb_v4` and `abdb_new_method` trees.
- The `step3.ipynb` model save location is relative, `./drive/MyDrive/@antigen_epitope/abdb_new_combine/`, and reaches the intended Drive location only from the expected working directory.

Update path assignments in a separate execution copy without changing research thresholds or algorithms. The public-facing configuration cannot be inferred by replacing just one root string: cross-project inputs, directory naming, and relative paths must be reviewed separately. Some cells assume output directories already exist, while others overwrite products or remove directories.

### Resource acquisition and provenance

| Resource | Preparation requirement |
| --- | --- |
| SAbDab metadata for the root preprocessing notebooks | Source comments give the [legacy SAbDab URL](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab/search/?all=true), which redirected during preparation to the current [SAbDab2 search page](https://sabdab.opig.stats.ox.ac.uk/search/?all=true). This does not identify the unknown historical snapshot; obtain the author-approved version separately. Required columns include `pdb`, `Hchain`, `Lchain`, `model`, `antigen_chain`, `antigen_type`. |
| PDB complexes for the SAbDab branch | Supply structures matching that metadata. Original retrieval cells use `Bio.PDB.PDBList` and download into `/content/tmp`; do not execute them during the data-free checks. Record identifiers, retrieval dates, and checksums. |
| AbDb PDBs for the `abdb_v2` branch | The preserved [abdb_v2/README.txt](../abdb_v2/README.txt) explicitly names [AbDb](http://www.abybank.org/abdb/) and records **“Kabat ==> NR”**. The URL timed out during preparation; current download availability was not verified. Exact snapshot, selection details, identifiers, and checksums remain unknown and need author confirmation. Do not substitute the SAbDab inputs merely because another branch uses them. |
| SI-encoded PDBs and interaction tables | Author-supplied prepared inputs are needed for the reviewed `abdb_new_combine` workflow. Confirm that B-factors were intentionally used to store SI and identify how contact labels were generated. No approved download URL has been established. |
| Folds and residue-patch text files | Obtain the exact five-fold definitions and positive/negative patch lists used by the selected experiment. Directory names are not evidence of a valid or disjoint evaluation split. |
| ESM weights | Obtain the selected model separately under its access conditions; loading a pretrained model may download weights. The code-only checks do not call pretrained loaders. |
| Trained classifier weights | Supply the matching fold models or explicitly retrain after the protocol is confirmed. No classifier weights are bundled and no external download endpoint has been established. |
| Example structures and figures | Historical examples refer to named PDB files and generated meshes/tables that are absent from this release. They are not ready-to-run fixtures. |

Before a scientific run, record source URLs or author-provided transfer locations, versions, checksums, file schemas, and permitted use for each resource. The repository does not redistribute these materials.

## Reviewed workflows

Cell numbers below are one-based and include empty cells. They identify the reviewed source stages; they are not a command to execute an entire notebook. Notebook outputs from earlier interactive sessions cannot establish that the current visible source ran successfully.

### A. Root structural preprocessing

1. **Select complexes.** Read the SAbDab TSV, retain nonempty antigen-chain entries, split `antigen_chain` and `antigen_type` on `|`, and retain protein antigens. The PDB retrieval/selection cells are Zhaoqian 14, Xiaohan 18, Yuhao 27, and `step2_colab` 12. Outputs are `data/structures/{pdb}_{H}_{L-or-nan}_{antigen}.pdb`. The metadata `model` column is read but no explicit model-number selection is applied by the chain selector.
2. **Select one contact definition.** Zhaoqian 17 / Xiaohan 26 / Yuhao 30 use non-hydrogen atom-pair distance ≤4.5 Å with a Cα distance prefilter of 15 Å. Although some titles mention side chains, this helper includes backbone heavy atoms. Zhaoqian 21 / Xiaohan 30 / Yuhao 33 instead use side-chain centers of mass at distance ≤7 Å. The alternatives write the same `antigen_info/{complex}_info.tsv`; running both overwrites the first result. `step2_colab` 15 implements the latter definition.
3. **Create surface inputs if required.** Xiaohan 21–22 and Yuhao 40–41 extract antigen-only PDBs into `antigen_pdbs/` and export PyMOL surfaces into `antigen_objs/`. Meshes are generated products and remain external.
4. **Select one SI implementation.** Xiaohan 25 uses 15 neighboring surface vertices for local triangulation/curvature, a centroid-based sign adjustment, and the nearest 10 surface vertices to assign residue SI. It exports `antigen_info_SI/{complex}_antigen_info_SI.tsv`. Yuhao 45 uses trimesh discrete curvature measures with radius 2 and a different formula/sign convention; it colors/displays the mesh but does not save an SI TSV. These branches must not be substituted for each other without author confirmation.
5. **Inspect outputs before continuing.** Common residue columns are `name`, `ResID`, `AA`, `SS`, `Cax`, `Cay`, `Caz`, `SCx`, `SCy`, `SCz`, `SaSaRate`, plus contact indicators `G,A,V,I,L,S,T,D,N,E,Q,K,R,C,M,F,Y,W,H,P`. `AA` uses three-letter residue names. SI tables contain `name`, `ResID`, `AA`, `SI`. Check chain identity, residue ordering, missing residues, and correspondence between positional SASA/secondary-structure lists and TSV rows using real fixtures.

`df.head(5)`/`df.head(100)` preview cells do not cap the retrieval loop because `filtered_df` was created earlier and is the object being iterated. Do not use them as a small-download switch. Missing `Lchain` entries may be NaN while the source calls `.strip()` after a truthiness check; review real metadata before treating all expected complexes as processed.

`secondary_structure.ipynb` is exploratory: its plot uses an embedded example list, and its B-factor export cell references `SaSaRate` without defining it. `step2_colab.ipynb` includes a PyMOL installation cell after an earlier PyMOL-dependent stage. These are documented limitations; repository cleanup does not choose missing scientific behavior on the author's behalf.

### B. `abdb_new_combine`: SI tables and ESM2

The two preparation notebooks overlap and have different inputs. Their numerical filenames do not define one required sequence.

| Notebook / stage | Input | Output / behavior |
| --- | --- | --- |
| `step1_part2_dataset_preparation.ipynb`, cell 5 | `data/antigen_pdb_with_SI/*.pdb` | Averages residue atomic B-factors as SI and writes `data/antigen_info_SI/*_info.tsv`. It first deletes the existing `antigen_info_SI` directory. |
| Same notebook, cell 7 | SI TSVs and `data/antigen_info/*_info.tsv` | Joins by `(ResID, AA)`, dropping duplicate SI keys, into `data/antigen_info_SI_interaction/`. |
| Same notebook, cells 12 and 14–15 | `data/antigen_info/`, not the merged directory | Writes `data/all_data_with_SI.csv`, then groups by `(ResID, AA)` without protein/chain, aggregates numeric columns by maximum, assigns the literal name `6vyb`, and overwrites the CSV. This is study-specific logic. SI is not guaranteed to be present. |
| `step2.ipynb`, cells 7–8 | `data/antigen_pdbs/*.pdb` and interaction TSVs | Extracts average-B-factor SI and merges it by `(ResID, AA)`. Duplicated merge keys can expand rows. |
| `step2.ipynb`, cell 9 | Merged residue tables | Constructs a sequence from standard amino acids in existing row order, derives interaction status, runs ESM2 layer 6, and adds `embedding_0` through `embedding_319`. Writes `data/all_antigen_info_SI/{original_tsv_name}_with_embeddings.tsv`. |
| `step2.ipynb`, cell 13 | Per-table embedding results | Concatenates to `data/all_data_with_SI.csv`. |

`Status` is `Interacting` when any of the 20 contact-indicator columns is nonzero. B-factor averaging is not itself a surface-geometry calculation: the meaning of the input B-factors must be established. Sequence order, chain separation, naming conventions, and duplicate `(ResID, AA)` keys need validation on the selected dataset. Empty directories and unknown residues are not handled as a general data-validation layer.

### C. `abdb_new_combine`: patch classifier

`step3.ipynb` reads five folds from **other project directories**, rather than directly consuming only the preceding notebook's local output:

```text
abdb_v4/fold_<1..5>/data_processed_step1_with_SI/
  cnn_positive_patch_3points.txt
  cnn_negative_patch_3points_part<1..4>.txt
abdb_new_method/fold_<1..5>/data/
  all_data_with_SI.csv
```

Patch text uses `Patches for protein NAME:` headings followed by `indices: [1, 2, 3]`-style lines. The code filters residues to `SaSaRate >= 0.1`, matches by protein `name` and integer `ResID`, and sums patch embeddings. Positives require exactly three matched embeddings; negatives require the matched count to equal the parsed patch size. The positional slice `iloc[0, -321:-1]` assumes the precise source column order; confirm it against the actual sibling-project CSV before training.

It writes `combined_positive_patches.csv`, `combined_negative_patches.csv`, and `classification_model_full_data.h5`. The classifier is Dense(128, ReLU) → Dropout(0.3) → Dense(64, ReLU) → Dense(1, sigmoid), trained with Adam, binary cross-entropy, accuracy, **100 epochs**, and **batch size 32**. Only the pandas shuffle uses `random_state=42`; TensorFlow/NumPy training seeds are not set. The training cell has no validation split or held-out evaluation. Do not infer deterministic training or independent validation from the fold-shaped input paths.

### D. `abdb_new_combine`: evaluation and visualization

`step4.ipynb` contains alternative evaluation blocks:

- Cell 9 reads five `abdb_new_method/fold_<1..5>/data_processed_step1_with_SI/classification_model_with_val.h5` models and evaluates the combined residue CSV after a `SaSaRate >= 0.2` filter; cell 10 summarizes successful folds.
- Cell 11 evaluates fold 2 only with `SaSaRate >= 0.1` as an alternative block. A later threshold change does not restore rows already discarded from a reused DataFrame.
- Cell 17 loads `abdb_new_combine/classification_model_full_data.h5` and uses `SaSaRate >= 0.1`.
- Cell 14 can write prediction-colored PDBs to `results/`, using the `merged_df` left by earlier execution. It reparses/overwrites files per residue and matches residues without antigen-chain identity. Antibody chains H/L are set to zero. The adjacent PyMOL instructions are application commands, not Python.

Evaluation sends **individual residue embeddings** to models trained here on **sums of patch embeddings**. The intended interpretation needs author confirmation. Some metrics use raw prediction ≥0.5, while others use within-protein min-max normalized scores or thresholded normalized scores. In the reviewed implementation, the primary ROC AUC uses normalized continuous scores; a separately printed ROC-curve AUC uses binary labels; balanced accuracy, MCC, and PR-AUC use thresholded normalized labels. Constant/all-null score groups are dropped after normalization. Preserve these conventions when describing existing behavior; changing them is a scientific modification.

Nonempty input, adequate score variation, and two label classes are assumed. Fold exceptions are printed and skipped, so reaching the final cell does not prove all five folds succeeded. No metric CSV is explicitly saved by the reviewed blocks. Capture fresh execution records and identify exactly which block produced each reported value in a future reproduction run.

### E. Incomplete ESM3 alternative

`abdb_new_combine/step2.5.ipynb` is not a required stage of the ESM2 workflow. It reads test-fold TSVs from `abdb_v4`, writes toward `abdb_new_combine`, and calls `ESM3.from_pretrained("esm3-open", device="cuda")`.

The per-file loop calls **`get_esm3_embedding()` without a definition or a sequence argument**. Its example sequence does not supply the missing per-file implementation. The historical install command requests `fair-esm`, which is not the separate SDK used by the ESM3 imports. Original saved output also showed a model-access error; that is historical context, not a current access test. This branch requires author-approved completion, compatible SDK/API versions, model access, and token/residue/dimension alignment before it can be described as runnable.

## Procedure for a future reproduction attempt

1. Identify the manuscript's exact notebook variants and cell branches, and record the repository commit. Resolve the contact/SI, `6vyb` aggregation, patch-to-residue inference, and metric conventions with the authors.
2. Build and lock a compatible research environment for each selected stage. Record OS, Python, CPU/GPU, CUDA if used, package versions, and pretrained model versions. Do not reuse the lightweight validation lock as a training environment.
3. Populate an external working tree with authorized, versioned inputs. Verify filenames, schemas, residue/chain mapping, embedding-column order, fold membership, and checksums before any deletion or overwrite cell is run.
4. Open a working copy in Jupyter/Colab, reconcile every input/output path, and select the required cells. Do not run alternative blocks into the same output locations. Avoid `Run all` and unattended full-notebook execution.
5. Validate one author-approved representative structure/sequence/patch path before larger processing. A representative fixture has not been supplied with this release; the synthetic smoke cases are not a substitute.
6. Run the selected preprocessing, embeddings, training, and evaluation stages while keeping fresh logs and outputs outside Git. Confirm the train/validation/test protocol independently and record any failures rather than silently treating skipped folds as success.
7. Compare the approved outputs against the paper's stated results only after the manuscript, expected values, and exact protocol are available. Document discrepancies and any approved scientific fixes separately from packaging changes.

## Required author decisions before public release

The paper metadata/citation, repository license, canonical research version, data/weight provenance, fold construction, complete environments, and accepted execution protocol remain to be confirmed. The first private release does not resolve these by choosing defaults or inventing manuscript information. End-to-end reproduction should be claimed only after fresh authorized execution with its inputs, versions, logs, and limitations recorded.
