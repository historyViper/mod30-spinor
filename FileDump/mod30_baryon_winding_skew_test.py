#!/usr/bin/env python3
"""
mod30_baryon_winding_skew_test.py

Diagnostic extension of mod30_complete_v2.py

Model tested:
    M_final =
      (M_geom + A * tri_wave(theta, 30 deg))
      * (1 + lambda_univ)
      * (1 + gamma * n_eff * skew/240)

Interpretation:
- tri_wave(theta, 30 deg): local Hamiltonian / sine-wave correction
- lambda_univ = GEO_BOUNDARY / ALPHA_QUARK: universal boundary projection
- n_eff * skew/240: toroid-shape skew weighted by winding number

This script uses fixed per-quark effective winding values extracted earlier
and averages them across the baryon's quark content.
"""

import importlib.util
from pathlib import Path
import numpy as np

BASE_FILE = Path("/mnt/data/mod30_complete_v2.py")
REPORT_FILE = Path("/mnt/data/mod30_baryon_winding_skew_test_report.txt")

# Effective quark winding values from earlier individual runs
# These are used as diagnostic labels/weights, not re-fitted here.
WINDING_EFF = {
    "up": 0.266619,
    "down": 0.233776,
    "strange": 2.063877,
    "bottom": 123.339835,
    "top": 0.166667,
    # charm intentionally omitted from the winding extraction fit
    # because charm had special cancellation structure
    # use 0.0 here so charm-sector behavior remains diagnostic
    "charm": 0.0,
}


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("mod30_complete_v2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tri_wave(theta_deg: float, segment_deg: float = 30.0) -> float:
    """
    Symmetric triangular wave in [-1, 1] built from segment_deg.
    """
    x = (theta_deg / segment_deg) % 2.0
    return 1.0 - 2.0 * abs(x - 1.0)


def baryon_winding_avg(quarks):
    vals = [WINDING_EFF.get(q, 0.0) for q in quarks]
    return float(np.mean(vals))


def evaluate_model(mod, A: float, gamma: float):
    rows = []

    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    scale = 1.0 + lambda_univ

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        pred, residue, delta_geo, delta_spin = mod.predict_baryon(quarks, J)
        skew = mod.skew_angle(quarks)
        theta = skew  # current proxy for local phase angle
        tri = tri_wave(theta, 30.0)
        n_eff = baryon_winding_avg(quarks)

        # local Hamiltonian correction inside geometry
        pred_with_local = pred + A * tri

        # global toroid-shape skew correction weighted by winding
        pred_final = pred_with_local * scale * (1.0 + gamma * n_eff * (skew / 240.0))

        err_pct = (pred_final - obs) / obs * 100.0
        abs_err_pct = abs(err_pct)

        rows.append({
            "name": name,
            "quarks": quarks,
            "obs": obs,
            "pred_final": pred_final,
            "err_pct": err_pct,
            "abs_err_pct": abs_err_pct,
            "skew": skew,
            "tri30": tri,
            "n_eff": n_eff,
            "sector": sector,
            "note": note,
        })

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}
    clean_rows = [r for r in rows if r["name"] not in charm_names and r["name"] not in omega_names]

    mape_all = float(np.mean([r["abs_err_pct"] for r in rows]))
    mape_clean = float(np.mean([r["abs_err_pct"] for r in clean_rows]))

    return {
        "A": A,
        "gamma": gamma,
        "rows": rows,
        "mape_all": mape_all,
        "mape_clean": mape_clean,
    }


def fit_best(mod):
    best = None

    # coarse-to-fine search around the values that previously worked well
    A_grid_1 = np.linspace(-10.0, 10.0, 801)
    g_grid_1 = np.linspace(-0.002, 0.002, 801)

    for A in A_grid_1:
        for gamma in g_grid_1[::10]:
            result = evaluate_model(mod, float(A), float(gamma))
            if best is None or result["mape_clean"] < best["mape_clean"]:
                best = result

    A0 = best["A"]
    g0 = best["gamma"]

    A_grid_2 = np.linspace(A0 - 1.0, A0 + 1.0, 801)
    g_grid_2 = np.linspace(g0 - 0.0006, g0 + 0.0006, 801)

    for A in A_grid_2:
        for gamma in g_grid_2[::8]:
            result = evaluate_model(mod, float(A), float(gamma))
            if result["mape_clean"] < best["mape_clean"]:
                best = result

    A0 = best["A"]
    g0 = best["gamma"]

    A_grid_3 = np.linspace(A0 - 0.3, A0 + 0.3, 601)
    g_grid_3 = np.linspace(g0 - 0.00012, g0 + 0.00012, 601)

    for A in A_grid_3:
        for gamma in g_grid_3[::6]:
            result = evaluate_model(mod, float(A), float(gamma))
            if result["mape_clean"] < best["mape_clean"]:
                best = result

    return best


def main():
    mod = load_module(BASE_FILE)

    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    scale = 1.0 + lambda_univ

    # Baseline: universal factor only
    baseline_rows = []
    for name, quarks, J, obs, sector, note in mod.BARYONS:
        pred, residue, delta_geo, delta_spin = mod.predict_baryon(quarks, J)
        pred_scaled = pred * scale
        err_pct = (pred_scaled - obs) / obs * 100.0
        baseline_rows.append({
            "name": name,
            "obs": obs,
            "err_pct": err_pct,
            "abs_err_pct": abs(err_pct),
        })

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}
    baseline_clean = [r for r in baseline_rows if r["name"] not in charm_names and r["name"] not in omega_names]
    baseline_mape_all = float(np.mean([r["abs_err_pct"] for r in baseline_rows]))
    baseline_mape_clean = float(np.mean([r["abs_err_pct"] for r in baseline_clean]))

    best = fit_best(mod)

    lines = []
    lines.append("=" * 84)
    lines.append("BARYON WINDING-WEIGHTED SKEW TEST")
    lines.append("=" * 84)
    lines.append("")
    lines.append(f"Base file:                {BASE_FILE.name}")
    lines.append(f"lambda_univ:              {lambda_univ:.8f}")
    lines.append(f"scale factor:             {scale:.8f}")
    lines.append("")
    lines.append("Model:")
    lines.append("  M_final = (M_geom + A * tri_wave(theta, 30 deg))")
    lines.append("            * (1 + lambda_univ)")
    lines.append("            * (1 + gamma * n_eff * skew/240)")
    lines.append("  with theta = skew_angle(quarks) as current phase proxy")
    lines.append("")
    lines.append("Baseline (universal factor only):")
    lines.append(f"  all-set MAPE:           {baseline_mape_all:.4f}%")
    lines.append(f"  clean-set MAPE:         {baseline_mape_clean:.4f}%")
    lines.append("")
    lines.append("Best fit:")
    lines.append(f"  A:                      {best['A']:.6f}")
    lines.append(f"  gamma:                  {best['gamma']:.9f}")
    lines.append(f"  all-set MAPE:           {best['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:         {best['mape_clean']:.4f}%")
    lines.append("")
    lines.append("-" * 84)
    lines.append("Per-baryon results")
    lines.append("-" * 84)
    header = f"{'Baryon':<10} {'Obs':>10} {'err%':>9} {'skew':>7} {'tri30':>8} {'n_eff':>12}"
    lines.append(header)
    lines.append("-" * len(header))

    for r in best["rows"]:
        tag = ""
        if r["name"] in omega_names:
            tag = " [omega]"
        elif r["name"] in charm_names:
            tag = " [charm]"
        lines.append(
            f"{r['name']:<10} {r['obs']:>10.3f} {r['err_pct']:>+9.3f} "
            f"{r['skew']:>7.1f} {r['tri30']:>8.3f} {r['n_eff']:>12.6f}{tag}"
        )

    lines.append("")
    lines.append("Fixed per-quark winding labels used:")
    for q, n in WINDING_EFF.items():
        lines.append(f"  {q:<8} -> {n:.6f}")
    lines.append("")
    lines.append("Notes:")
    lines.append("- clean set excludes Omega- and charm-sector baryons")
    lines.append("- charm uses n_eff = 0.0 here so charm-sector remains diagnostic")
    lines.append("- local 30 deg term is interpreted as Hamiltonian / sine-wave correction")
    lines.append("- winding-weighted skew is interpreted as toroid-shape correction")
    lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("")
    print(f"Saved report to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
