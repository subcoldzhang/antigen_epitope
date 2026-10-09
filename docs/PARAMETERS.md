# Embedded research-parameter index

This is a read-only index of important values found in the notebook source, reviewed on 2026-10-09. It covers selected structural, embedding, classifier, and evaluation branches; it is not an exhaustive extraction of every constant in every historical notebook. **There is no shared configuration loader, and this document does not change runtime behavior.**

Each location uses a repository-relative path and the **original one-based cell number, including empty cells**. `abdb_new_combine/step4.ipynb` refers to the originally extensionless `step4` notebook. Source cleanup and filename mapping are documented separately in [CURATION.md](CURATION.md) and [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).

The collection contains distinct experiments, not one set of project defaults. In particular, do not unify 4.5 Å and 7 Å contact rules, SI formulas, `SaSaRate > 0.1` and `>= 0.1`, 0.1 and 0.2 filters, or raw and normalized score cutoffs during packaging. The authors must identify which source version and execution order correspond to the paper. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the input/output and execution implications.

## Structure selection and contact definitions

| Location | Embedded setting | Interpretation / scope |
| --- | --- | --- |
| `step1_colab_zhaoqian.ipynb`, cell 14; `step1_colab_xiaohan_add_SI.ipynb`, cell 18; `step1_part1_mesh_SI_calculation_yuhao.ipynb`, cell 27; `step2_colab.ipynb`, cell 12 | `antigen_type == 'protein'`; antigen chain/type lists split on `\|` | PDB-selection branch. The metadata `model` column is read but not used to select a specific model by number. |
| `step1_colab_zhaoqian.ipynb`, cell 17; `step1_colab_xiaohan_add_SI.ipynb`, cell 26; `step1_part1_mesh_SI_calculation_yuhao.ipynb`, cell 30 | `cutoff_distance=4.5`, `ca_cutoff_distance=15` | Distances in Å. A contact is any non-hydrogen atom pair at distance ≤4.5 Å, after excluding residue pairs with Cα distance >15 Å. Backbone heavy atoms are included despite side-chain wording in some titles. |
| `step1_colab_zhaoqian.ipynb`, cell 21; `step1_colab_xiaohan_add_SI.ipynb`, cell 30; `step1_part1_mesh_SI_calculation_yuhao.ipynb`, cell 33; `step2_colab.ipynb`, cell 15 | Side-chain center-of-mass distance `<= 7` | A separate label definition; glycine uses its Cα coordinate in the batch helper. It writes the same contact-table paths as the 4.5 Å branch in notebooks containing both. |
| `step1_colab_xiaohan_add_SI.ipynb`, cell 17 | `df.head(5)` | Preview/scratch assignment only; the retrieval loop uses the previously created `filtered_df`. This is not a five-structure download limit. |
| `step1_colab_zhaoqian.ipynb`, cell 13; `step1_part1_mesh_SI_calculation_yuhao.ipynb`, cell 26; `step2_colab.ipynb`, cell 11 | `df.head(100)` | Same distinction: it does not restrict the existing `filtered_df` loop. |

## Surface shape-index variants

| Location | Embedded setting | Interpretation / scope |
| --- | --- | --- |
| `step1_colab_xiaohan_add_SI.ipynb`, cell 25 | `n_neighbors=15` | Neighborhood used for local surface triangulation and curvature. |
| Same cell | `elem < 0` replaced by `1e-8`; `SI = (-2/π) * atan((k1+k2)/(k1-k2))` | Numerical guard and initial SI formula, followed by a centroid-distance-based sign adjustment. |
| Same cell | `n_neighbors=10`; mean of nearest surface-vertex SI values | Maps mesh values to residue Cα positions and exports an SI TSV. |
| `step1_part1_mesh_SI_calculation_yuhao.ipynb`, cell 45 | Discrete Gaussian/mean curvature radius `2`; `elem <= 0` replaced by `1e-8`; `SI = (2/π) * atan((k1+k2)/(k1-k2))` | Distinct trimesh method and sign convention. Stores SI in mesh attributes, colors using `coolwarm`, and displays the mesh; the cell does not save an SI TSV. |
| `step1_colab_zhaoqian.ipynb`, cell 26; `step1_colab_xiaohan_add_SI.ipynb`, cell 35 | `thresholds=[0.1, 0.2, 0.3]` with `SaSaRate > threshold` | Exploratory curvature sweep, not a selected manuscript default. |
| `step1_colab_zhaoqian.ipynb`, cell 29; `step1_colab_xiaohan_add_SI.ipynb`, cell 38 | Function defaults `n_neighbors=3`, `threshold=0.1`; execution lists `[12,16,20]` and `[0.1]` | The actual loop overrides the function's neighbor default. Preserve both definitions and call sites. |

## SI-table preparation and protein embeddings

| Location | Embedded setting | Interpretation / scope |
| --- | --- | --- |
| `abdb_new_combine/step1_part2_dataset_preparation.ipynb`, cell 5; `abdb_new_combine/step2.ipynb`, cell 7 | Residue SI = mean atomic B-factor | Requires prior SI encoding in the input PDB. This is extraction, not a standalone geometry method. The two notebooks read different PDB directories. |
| `abdb_new_combine/step1_part2_dataset_preparation.ipynb`, cells 14–15 | Group by `(ResID, AA)`; numeric aggregation `max`; assign `name='6vyb'` | Study-specific grouping without protein/chain keys, overwriting `all_data_with_SI.csv`. Do not generalize it as data cleanup. |
| `abdb_new_combine/step2.ipynb`, cell 5 | `esm2_t6_8M_UR50D()`; `.eval()` | ESM2 model choice. Pretrained loading can download external weights. No explicit CUDA move in this branch. |
| Same notebook, cell 6 | `repr_layers=[6]`, `return_contacts=True`, `torch.no_grad()`, token slice `1 : batch_lens[0]-1` | Uses layer 6 residue representations after dropping special boundary tokens. |
| Same notebook, cell 9; `abdb_new_combine/step3.ipynb`, cell 7 | Per-residue `embedding_0..319`; patch `Embedding_1..320` | 320-value embedding interface used by downstream code. Feature-column naming differs between residue and patch tables. |
| `abdb_new_combine/step2.ipynb`, cell 9 | Sum of 20 contact indicators equals zero → `Non-Interacting`; otherwise `Interacting` | Label creation. Sequence construction uses the existing table row order and standard-amino-acid mapping. |
| `abdb_new_combine/step2.5.ipynb`, cell 5 | `ESM3.from_pretrained('esm3-open', device='cuda')`; `SamplingConfig(return_per_residue_embeddings=True)` | Incomplete separate ESM3 experiment, not a substitute for ESM2. |
| Same notebook, cell 6 | `range(1,6)`; undefined `get_esm3_embedding()` called with no arguments | Five test-fold loop, but no working sequence-to-embedding implementation is supplied. No valid ESM3 embedding dimension is established by this loop. |

## Patch preparation and dense classifiers

| Location | Embedded setting | Interpretation / scope |
| --- | --- | --- |
| `abdb_new_combine/step3.ipynb`, cells 3 and 5 | Folds `range(1,6)`; `SaSaRate >= 0.1`; feature slice `iloc[0,-321:-1]` | Reads sibling-project files and assumes their exact column ordering. These are not automatically the local `step2` outputs. |
| Same notebook, cell 3 | Exactly `3` matched positive residue embeddings; sum across residues | Patch feature construction; no averaging. |
| Same notebook, cell 5 | Negative parts `range(1,5)`; match count must equal patch index count; sum embeddings | Four negative-patch files per fold. Deduplicates by `(Protein_Name, Patch_Indices)`. |
| Same notebook, cell 7 | Shuffle `random_state=42`; positive→1, negative→0 | Sets the table-shuffle seed only, not all framework/random states. |
| Same notebook, cell 7 | Dense `128` ReLU → Dropout `0.3` → Dense `64` ReLU → Dense `1` sigmoid | Full-data classifier architecture. |
| Same notebook, cell 7 | Adam; binary cross-entropy; accuracy; `epochs=100`; `batch_size=32` | No explicit optimizer learning rate, validation split, or early stopping here. Historical library-default values must not be invented. |
| `abdb_new_method/step3_part1.ipynb` through `step3_part5.ipynb`, cell 10 | `test_size=0.2`, `random_state=42`; shuffle seed 42 | Separate per-fold dense-classifier branch with a train/validation split. A random row split does not by itself establish protein-level independence. |
| Same five notebooks, cell 10 | Same 128/64/1 dense widths, dropout 0.3; Adam/binary cross-entropy; up to 100 epochs; batch 32 | This branch additionally uses `EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)`. Do not copy early stopping into the full-data branch without recording a scientific change. |

## Selected historical fold/CNN settings

These examples document additional preserved versions. They are not defaults for the ESM/dense workflow.

| Location | Embedded setting | Interpretation / scope |
| --- | --- | --- |
| `abdb_v4/step0.ipynb`, cell 6 | `n_splits=5`; `KFold(n_splits=n_splits)` | PDB list is built from `os.listdir` without an explicit sort. No shuffle argument or random seed is supplied to `KFold` here; exact fold membership requires the original file list/order or saved split manifest. |
| `abdb_v4/step1_part3_prepare_dataset_with_SI.ipynb`, cells 6 and 10 | `SaSaRate > 0.1` | Strict comparison; distinct from downstream `>= 0.1`. |
| `abdb_v4/step1_prepare_negative_dataset_with_SI_part1.ipynb`, cell 6; parts 2–4, cell 3 | Non-interacting residues with `SaSaRate > 0.1` | Source negative-patch selection threshold. |
| `abdb_v4/step2_CNN_Patch_classification_3points_SasaRate_with_SI_1.ipynb`, cells 16–17 | Batch `500`; initial `LR=0.001`; split `test_size=0.2`, `random_state=1000`; train/test loaders both `shuffle=True` | Example CNN fold variant. Device is CUDA if available, otherwise CPU. |
| Same notebook, cell 22 | `LR=0.0001`; Adam; `BCELoss` | This reassignment overrides the earlier 0.001 value when executed in order. Listing only the “Hyper Parameters” cell would misstate the optimizer setup. |
| `abdb/step2_CNN_Patch_classification_3points_SasaRate.ipynb`, cells 7, 18–19, and 24 | NumPy seed `42`; batch `500`; `LR=0.001`; split `test_size=0.2`, `random_state=1000`; Adam/`BCELoss` | A different historical CNN branch. These values do not replace the settings in `abdb_v4` or the dense classifiers. |

## Evaluation filters, scores, and thresholds

| Location | Embedded setting | Interpretation / scope |
| --- | --- | --- |
| `abdb_new_combine/step4.ipynb`, cell 9 | Folds `1..5`; initial `SaSaRate >= 0.2`; later `>= 0.1` on the already filtered table | Effective retained data cannot include the rows removed by the first filter. Uses sibling-project fold models. |
| Same notebook, cell 11 | Fold `2` only (`range(2,3)`); `SaSaRate >= 0.1` | Alternative evaluation block. |
| Same notebook, cell 17 | Full-data model; `SaSaRate >= 0.1` | Another alternative; supplies individual 320-value residue embeddings to a classifier trained on summed patch embeddings. |
| Same notebook, cells 9, 11, 17 | Within-`name` min-max score normalization | Constant or entirely missing groups become NaN and are removed. |
| Same cells | Raw prediction `>=0.5` | Accuracy, precision, recall, and F1 use this raw-score decision. |
| Same cells | Normalized continuous scores for primary ROC AUC | Distinct from the separately plotted ROC-curve AUC, which uses binary decisions in source. |
| Same cells | Normalized score `>=0.5` | Balanced accuracy, MCC, and the reported PR-AUC use this binary decision in source. Do not silently replace it with continuous-score PR-AUC. |

For a paper release, record a compact manifest of the **chosen** notebook paths, commit, cell branches, input versions, and effective parameter values after any reassignments. Confirm that selection with the authors. This index preserves differing source choices and does not designate any historical branch as the successful or final experiment.
