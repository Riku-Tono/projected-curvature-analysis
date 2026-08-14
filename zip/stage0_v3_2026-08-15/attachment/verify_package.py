from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "projected_curvature_repro_mpl"))

import matplotlib.image as mpimg
import numpy as np


ROOT = Path(__file__).resolve().parent
REFERENCE_FILES = [
    "projected_curvature_result.json",
    "taylor_coefficients.csv",
    "mode_group_curvature_contributions.csv",
    "active_disk_quadratic_demand.csv",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def close_number(left: float, right: float) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    return math.isclose(left, right, rel_tol=2e-12, abs_tol=2e-11)


def compare_json(left: Any, right: Any, path: str = "root") -> list[str]:
    failures: list[str] = []
    if isinstance(left, bool) or isinstance(right, bool):
        if left is not right:
            failures.append(path)
    elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if not close_number(float(left), float(right)):
            failures.append(path)
    elif isinstance(left, dict) and isinstance(right, dict):
        if set(left) != set(right):
            failures.append(path + ".keys")
        for key in sorted(set(left) & set(right)):
            failures.extend(compare_json(left[key], right[key], f"{path}.{key}"))
    elif isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            failures.append(path + ".length")
        for index, (lvalue, rvalue) in enumerate(zip(left, right)):
            failures.extend(compare_json(lvalue, rvalue, f"{path}[{index}]"))
    elif left != right:
        failures.append(path)
    return failures


def maybe_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def compare_csv(reference: Path, replay: Path) -> list[str]:
    with reference.open(encoding="utf-8", newline="") as handle:
        expected = list(csv.DictReader(handle))
    with replay.open(encoding="utf-8", newline="") as handle:
        actual = list(csv.DictReader(handle))
    failures: list[str] = []
    if len(expected) != len(actual):
        return [f"row_count:{len(expected)}!={len(actual)}"]
    for index, (left, right) in enumerate(zip(expected, actual)):
        if set(left) != set(right):
            failures.append(f"row[{index}].columns")
            continue
        for key in left:
            lnumber = maybe_float(left[key])
            rnumber = maybe_float(right[key])
            if lnumber is not None and rnumber is not None:
                if not close_number(lnumber, rnumber):
                    failures.append(f"row[{index}].{key}")
            elif left[key] != right[key]:
                failures.append(f"row[{index}].{key}")
    return failures


def check_manifest() -> tuple[bool, int, list[str]]:
    failures: list[str] = []
    entries = 0
    for line in (ROOT / "MANIFEST_SHA256.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        entries += 1
        path = ROOT / name
        if not path.is_file() or sha256(path) != digest:
            failures.append(name)
    return not failures, entries, failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify package integrity and replay the sealed read-only analysis.")
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args()
    tests: list[tuple[str, bool, str]] = []

    manifest_pass, manifest_entries, manifest_failures = check_manifest()
    tests.append(("manifest", manifest_pass, ",".join(manifest_failures)))

    solve_paths = sorted((ROOT / "inputs" / "solves").glob("solve_*.json"))
    tests.append(("source_solve_count", len(solve_paths) == 38, str(len(solve_paths))))
    solve_records = [json.loads(path.read_text(encoding="utf-8")) for path in solve_paths]
    tests.append(("all_source_solves_pass", all(row["status"] == "PASS" for row in solve_records), ""))
    tests.append(("source_package_verification", "PACKAGE VERIFICATION: PASS" in (ROOT / "inputs" / "source_metadata" / "PACKAGE_VERIFICATION.txt").read_text(encoding="utf-8"), ""))
    tests.append(("reference_package_verification", "PACKAGE VERIFICATION: PASS" in (ROOT / "reference" / "PACKAGE_VERIFICATION.txt").read_text(encoding="utf-8"), ""))

    with np.load(ROOT / "inputs" / "frozen_maps.npz", allow_pickle=False) as maps:
        shapes_ok = (
            maps["a_coeff"].shape == (3, 30, 16)
            and maps["b_coeff"].shape == (3, 30, 16)
            and maps["q0"].shape == (16,)
            and maps["q2"].shape == (16,)
            and maps["ell_list"].tolist() == [0, 2, 4]
        )
        structure_ok = np.flatnonzero(maps["q0"]).tolist() == [0] and float(maps["q2"][0]) == 0.0
    tests.append(("frozen_map_shapes", shapes_ok, ""))
    tests.append(("frozen_projection_structure", structure_ok, ""))

    reference_result = json.loads((ROOT / "reference" / "projected_curvature_result.json").read_text(encoding="utf-8"))
    reference_invariants = (
        reference_result["source_solve_count"] == 38
        and reference_result["new_solver_runs"] == 0
        and reference_result["classification"] == "PARTIALLY_EXPLAINED"
        and reference_result["ell0_sigma_mode_identity"]["sigma_reconstruction_relative_residual"] < 1e-10
    )
    tests.append(("sealed_reference_invariants", reference_invariants, ""))

    exact_matches = 0
    semantic_matches = 0
    replay_error = ""
    with tempfile.TemporaryDirectory(prefix="curvature_repro_") as temporary:
        temp_root = Path(temporary)
        replay_dir = temp_root / "replayed"
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["MPLCONFIGDIR"] = str(temp_root / "mplconfig")
        completed = subprocess.run(
            [sys.executable, "-B", str(ROOT / "src" / "reproduce.py"), "--output-dir", str(replay_dir)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        replay_ok = completed.returncode == 0
        replay_error = (completed.stdout + completed.stderr).strip()
        tests.append(("replay_command", replay_ok, replay_error if not replay_ok else ""))
        if replay_ok:
            expected_json = json.loads((ROOT / "reference" / "projected_curvature_result.json").read_text(encoding="utf-8"))
            actual_json = json.loads((replay_dir / "projected_curvature_result.json").read_text(encoding="utf-8"))
            json_failures = compare_json(expected_json, actual_json)
            if sha256(ROOT / "reference" / "projected_curvature_result.json") == sha256(replay_dir / "projected_curvature_result.json"):
                exact_matches += 1
            if not json_failures:
                semantic_matches += 1
            tests.append(("replayed_result_json", not json_failures, ",".join(json_failures[:10])))

            for name in REFERENCE_FILES[1:]:
                failures = compare_csv(ROOT / "reference" / name, replay_dir / name)
                if sha256(ROOT / "reference" / name) == sha256(replay_dir / name):
                    exact_matches += 1
                if not failures:
                    semantic_matches += 1
                tests.append((f"replayed_{name}", not failures, ",".join(failures[:10])))

            expected_png = ROOT / "reference" / "projected_curvature_decomposition.png"
            actual_png = replay_dir / "projected_curvature_decomposition.png"
            pixel_exact = actual_png.is_file() and sha256(expected_png) == sha256(actual_png)
            shape_ok = actual_png.is_file() and mpimg.imread(expected_png).shape == mpimg.imread(actual_png).shape
            tests.append(("replayed_plot", shape_ok, f"pixel_exact={pixel_exact}"))

    pass_count = sum(int(passed) for _, passed, _ in tests)
    status = "PASS" if pass_count == len(tests) else "FAIL"
    lines = [
        f"PACKAGE VERIFICATION: {status}",
        f"tests={pass_count}/{len(tests)}",
        f"manifest_entries={manifest_entries}",
        "source_solve_count=38",
        "new_solver_runs=0",
        f"regenerated_numeric_artifacts_semantic_match={semantic_matches}/4",
        f"regenerated_numeric_artifacts_exact_hash_match={exact_matches}/4",
        "plot_policy=numeric_source_verified; PNG dimensions required; pixel hash diagnostic only",
    ]
    for name, passed, detail in tests:
        lines.append(f"[{ 'PASS' if passed else 'FAIL' }] {name}" + (f": {detail}" if detail else ""))
    report = "\n".join(lines) + "\n"
    print(report, end="")
    if args.write_report:
        target = args.write_report if args.write_report.is_absolute() else ROOT / args.write_report
        target.write_text(report, encoding="utf-8")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
