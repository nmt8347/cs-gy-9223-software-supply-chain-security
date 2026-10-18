# Rekor Verifier

Command-line tool that verifies entries and state of the Sigstore Rekor public transparency log (`https://rekor.sigstore.dev`). Built for NYU CS-GY 9223, Software Supply Chain Security.

## Functionality

| Operation | Description |
|---|---|
| Checkpoint retrieval | Fetches the latest signed tree head (tree ID, tree size, root hash) from Rekor. |
| Inclusion verification | Given a log index and an artifact file: pulls the entry, extracts the signing certificate and signature, verifies the artifact signature (ECDSA / SHA-256), then verifies the entry's Merkle inclusion proof against the log root. |
| Consistency verification | Given a previously saved checkpoint, fetches the latest checkpoint and a consistency proof from Rekor, then verifies the old tree is a prefix of the new tree (RFC 6962). |

## Requirements

- Python >= 3.11
- Network access to `rekor.sigstore.dev`
- Dependencies: `requests`, `cryptography`

## Installation

With Poetry (recommended; `package-mode = false`, dependencies only):

```bash
poetry install
poetry run python main.py --help
```

With pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests cryptography
```

## Usage

```
python3 main.py [-d] [-c] [--inclusion LOG_INDEX --artifact PATH]
                [--consistency --tree-id ID --tree-size N --root-hash HEX]
```

| Flag | Purpose |
|---|---|
| `-d`, `--debug` | Verbose output. Also writes the latest checkpoint to `checkpoint.json`. |
| `-c`, `--checkpoint` | Print the latest checkpoint as JSON. |
| `--inclusion LOG_INDEX` | Verify inclusion of the entry at `LOG_INDEX`. Requires `--artifact`. |
| `--artifact PATH` | Artifact file whose signature is verified against the entry. |
| `--consistency` | Verify a previous checkpoint against the latest one. Requires the three flags below. |
| `--tree-id ID` | Tree ID of the previous checkpoint. |
| `--tree-size N` | Tree size of the previous checkpoint. |
| `--root-hash HEX` | Root hash of the previous checkpoint, hex encoded. |

### Examples

Get the latest checkpoint:

```bash
python3 main.py -c
```

Verify inclusion of an entry for the bundled sample artifact:

```bash
python3 main.py --inclusion 3256683300 --artifact artifact.md
```

Expected final line on success:

```
Successfully verified inclusion of log index 3256683300 for artifact 'artifact.md'.
```

Verify consistency of an older checkpoint with the current log:

```bash
python3 main.py --consistency \
  --tree-id 1193050959916656506 \
  --tree-size 3179970807 \
  --root-hash 7d11ecb2538fcb98aae1405d31a2df1416e89a5f96045ba2feb05057067eea8f
```

Expected final line on success:

```
Consistency verification successful.
```

Typical workflow: run `-c`, save `treeID`, `treeSize`, `rootHash`, later run `--consistency` with those values.

## Project Layout

```
.
├── main.py                      CLI, Rekor API calls, inclusion and consistency orchestration
├── merkle_proof.py              RFC 6962 hashing, inclusion proof and consistency proof verification
├── util.py                      Certificate public key extraction, artifact signature verification
├── artifact.md                  Sample signed artifact
├── artifact_sigstore.json       Sigstore bundle for the sample artifact (certificate, tlog entry, timestamp)
└── pyproject.toml               Dependencies and tool configuration
```

## How Verification Works

**Inclusion**

1. Fetch the entry via `GET /api/v1/log/entries?logIndex=N`.
2. Decode the base64 `body`; read the signature and the PEM certificate from `spec.signature`.
3. Extract the public key from the certificate and verify the signature over the artifact bytes (ECDSA, SHA-256).
4. Compute the leaf hash: `SHA256(0x00 || decoded body)`.
5. Recompute the root from the leaf hash and `inclusionProof.hashes`, compare with `inclusionProof.rootHash`.

**Consistency**

1. Validate the supplied checkpoint (`size >= 1`, latest size >= supplied size, tree IDs match).
2. Fetch the proof via `GET /api/v1/log/proof?firstSize=..&lastSize=..&treeID=..` (skipped when sizes are equal).
3. Recompute both the old and new roots from the proof and compare with the supplied and latest root hashes.

## Development

Install dev tools:

```bash
poetry install --with dev
```

Tooling configured in `pyproject.toml` (line length 88):

```bash
poetry run black .                          # format
poetry run flake8                           # lint
poetry run mypy                             # type check (main.py, merkle_proof.py, util.py)
poetry run bandit -c pyproject.toml -r .    # security scan
```

Module responsibilities:

- Hashing and proof math belong in `merkle_proof.py`. Keep it free of network and file I/O.
- Key and signature handling belong in `util.py`.
- Network access and CLI wiring belong in `main.py`.