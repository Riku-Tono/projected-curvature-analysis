# 90°/270° projected-curvature mechanism: reproducible read-only package

This repository replays a sealed, read-only analysis of 38 previously saved support solves. It explains where the common projected-curvature radius scale near 47 comes from and separates the structurally explained scale from the unresolved upper-cap cancellation.

**Classification:** `PARTIALLY_EXPLAINED`  
**Saved source solves:** 38  
**New solver runs:** 0

![Curvature decomposition](reference/projected_curvature_decomposition.png)

## Main result

On the frozen grid, the ell=0 imaginary-amplitude map satisfies

```text
B0 c_sigma = sigma(s)
```

with relative residual `1.3177829497399766e-14`. Defining

```text
kappa_sigma = q2_ell0^T c_sigma = 0.005280296954172882
```

and using the unitarity-disk expansion gives

```text
rho = 1 / (4 kappa_sigma) = 47.34582205692646.
```

The saved finite-window fits are `47.34266132851574` at 270° and `47.13790398372574` at 90°. The lower result is reproduced by the structural scale to about `0.00668%`; the upper quadratic coefficient differs from it by `0.44108%` after a large cross-ell cancellation. No exact full-feasible-set identity was found that forces that cancellation.

## Quick verification

Python 3.14.5 was used for the sealed replay. After creating an environment:

```bash
python -m venv .venv
```

Activate it, then install the lock file and run the one-command verifier:

```bash
python -m pip install -r requirements.lock.txt
python verify_package.py
```

The verifier checks every manifest entry, validates all 38 saved solves, regenerates the result JSON and three CSV records in a temporary directory, and compares them with the sealed reference artifacts.

To retain a local replay:

```bash
python src/reproduce.py --output-dir reproduced
```

## Reproducibility boundary

This package reproduces the read-only second-order analysis from the 38 saved solver outputs. It deliberately does **not** rerun the SDP/support solver, refine parameters, change the ell truncation, or make a continuum-limit claim. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the exact replay and verification contract.

Raw coefficient norms are not used as physical mode weights. The reported group norms and disk demands are constructed in physical-amplitude space or as projected coordinate-invariant quantities.

## Repository layout

```text
inputs/solves/              38 immutable saved solve records
inputs/frozen_maps.npz      portable frozen linear maps used by the replay
inputs/source_metadata/     source-package fingerprints and verification
inputs/upstream_snapshots/  provenance snapshots used to construct the maps
reference/                  sealed analysis outputs
src/reproduce.py            solver-free replay
verify_package.py           integrity + independent replay verifier
MANIFEST_SHA256.txt         file-level package hashes
```

No license is asserted by this package. Add an appropriate license before publishing if redistribution terms are required.
