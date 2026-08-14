# Reproducibility contract

## What is replayed

`src/reproduce.py` reads only:

- the 38 JSON records under `inputs/solves/`;
- `inputs/frozen_maps.npz`, containing the frozen real/imaginary amplitude maps, grids, projection vectors, ell list, mass, and variable count.

It regenerates:

- `projected_curvature_result.json`;
- `taylor_coefficients.csv`;
- `mode_group_curvature_contributions.csv`;
- `active_disk_quadratic_demand.csv`;
- `projected_curvature_decomposition.png`.

No optimization package is imported by the replay. No solver call, parameter refinement, support-direction addition, or ell refinement occurs.

## One-command verification

From the package root:

```bash
python verify_package.py
```

The verifier performs four layers:

1. Checks every file listed in `MANIFEST_SHA256.txt`.
2. Confirms 38/38 saved solve records have `status=PASS` and both upstream package-verification records say PASS.
3. Runs the replay in a fresh temporary directory.
4. Compares the regenerated JSON and all three CSVs with their sealed counterparts. Exact hashes are reported when available; tight semantic floating-point comparison is the cross-platform release criterion.

The plot is regenerated from the already verified numerical sources. PNG dimensions are required to match; pixel hashes are diagnostic because font rendering can legitimately differ across operating systems.

## Dependency policy

- `requirements.lock.txt` records the complete Python dependency set used for package validation.
- `requirements.txt` gives the minimal direct dependencies.
- `.python-version` records the validation interpreter.

The replay requires no network after dependencies have been installed.

## Frozen-map provenance

`inputs/frozen_maps.npz` is a portable snapshot derived from the copied upstream files in `inputs/upstream_snapshots/`. Those snapshots are not imported by the standard replay; they are included so that the exact source coefficient array, projection record, configuration, and reconstruction-code versions remain auditable.

`PROVENANCE.json` records logical source names and SHA-256 hashes without relying on the original Windows paths.

## Claim boundary

The package establishes reproducibility for this frozen finite-grid analysis only. It does not prove differentiability, an exact upper/lower feasible-set symmetry, convergence in ell or grid resolution, or an asymptotic continuum curvature. The active-constraint ranking is an unweighted physical disk-demand ranking because conic dual multipliers were not saved.
