# Core experiment inputs

The [2026-11-08 data release](https://github.com/subcoldzhang/antigen_epitope/releases/tag/data-core-2026-11-08) contains **1,261 existing files, totaling 1,205,977,471 uncompressed bytes** (1.21 GB). The single `core-experiment-inputs.tar.gz` download is **277,243,644 bytes** (277 MB). It preserves original relative paths and file contents from the author's research directory. The snapshot date is the packaging date; the source acquisition dates remain unknown.

The repository is private, so an account with access is required. Data are distributed as Release assets. A normal Git clone or GitHub's automatic source-code ZIP does not include the data payload.

## Contents

| Location | Files | Contents |
| --- | ---: | --- |
| `abdb_v3/pdb/` | 1,151 | Existing AbDb PDB structures. |
| `abdb_new_combine/data/` | 36 | Existing external-test PDB structures and TSV/CSV tables, excluding OBJ meshes. |
| `abdb_v4/fold_*/` | 74 | Available direct text/CSV inputs: combined residue tables, negative-part tables, positive/negative/testing patch definitions, testing-patch indices, and processed-protein lists. |

[DATA_FILES.tsv](DATA_FILES.tsv) records every included file's relative path, byte size, SHA-256, and archive. The Release's `SHA256SUMS` records the compressed archive checksum:

```text
1eb793d5e4035ea3b216aef194a52c07915c2a413a1d4e4f0d7299e14b4507c5  core-experiment-inputs.tar.gz
```

[DATA_FOLD_MEMBERSHIP.tsv](DATA_FOLD_MEMBERSHIP.tsv) records the 4,834 PDB filenames actually present in the original fold directories. Repeated train/test PDB copies from those directories are represented by this inventory rather than duplicated in the archive. Membership is a directory snapshot; it does not certify the manuscript's final split or train/test independence.

## Download and extract

Download `core-experiment-inputs.tar.gz` and `SHA256SUMS` from the Release page, or use an authenticated [GitHub CLI](https://cli.github.com/):

```sh
# Run from the repository root. Choose a separate data workspace.
mkdir -p .data-download ../antigen_epitope-core-data
gh release download data-core-2026-11-08 \
  --repo subcoldzhang/antigen_epitope \
  --dir .data-download \
  --pattern core-experiment-inputs.tar.gz --pattern SHA256SUMS

# macOS; on Linux use sha256sum -c SHA256SUMS instead.
(cd .data-download && shasum -a 256 -c SHA256SUMS) &&
  tar -xzf .data-download/core-experiment-inputs.tar.gz \
    -C ../antigen_epitope-core-data
```

Allow approximately 1.21 GB for extracted files, plus 277 MB for the download. Extraction creates `abdb_v3/pdb/`, `abdb_new_combine/data/`, and `abdb_v4/fold_*/` under the chosen workspace. Point the selected notebook's existing path assignments there; the notebooks do not automatically discover these downloads. The archive can also be extracted at a checkout root if that is the intended layout.

## Known gaps and exclusions

- The original `abdb_v4/fold_2/data/` directory is empty. Its training PDB directory and `all_data_with_SI.csv` are absent. Other existing fold-2 patch files and test inputs are included. No files or memberships were reconstructed.
- Historical SAbDab structures and tables under root `data/` are excluded from this release, along with the approximately 80 GB OBJ mesh collection, other OBJ files, NPY feature/tensor caches, model weights, evaluation results, package binaries, copied reference PDFs, other historical versions' data, and `abdb_new_method` embedding inputs. Source notebooks remain in Git.
- The canonical manuscript variant and relationship of these files to reported results still need to be established. Packaging existing files does not validate their scientific labels or completeness.

File counts, byte sizes, and SHA-256 values were checked between the copied files, manifest, and every archive member. This update did not execute research notebooks, regenerate features, train models, or establish experimental reproduction. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for execution constraints.
