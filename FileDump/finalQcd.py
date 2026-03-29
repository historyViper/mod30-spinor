#!/usr/bin/env python3
"""
mod30_baryon_dual_angle_vortex_test.py

Tests a dual-angle local correction model on top of mod30_complete_v2.py

Model:
    tri_geom   = tri_wave(theta, phi_geom)
    vortex_int = 1 - abs(tri_wave(theta, phi_int))

    delta_geo_new = delta_geo + A * tri_geom + B * vortex_int

    M_final = (M_geom - delta_geo + delta_geo_new) * (1 + lambda_univ)

Interpretation:
- phi_geom : geometric/toroid angle
- phi_int  : interaction/cancellation angle
- A        : triangle/toroid amplitude
- B        : central-vortex amplitude

Current proxy:
- theta = skew_angle(quarks)

This is a diagnostic script. It does not modify the base framework.
"""

import importlib.util
from pathlib import Path
import numpy as np

BASE_FILE = Path("/mnt/data/mod30_complete_v2.py")
REPORT_FILE = Path("/mnt/data/mod30_baryon_dual_angle_vortex_test_report.txt")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("mod30_complete_v2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tri_wave(theta_deg: float, segment_deg: float) -> float:
    """
    Symmetric triangular wave in [-1, 1].
    """
    x = (theta_deg / segment_deg) % 2.0
    return 1.0 - 2.0 * abs(x - 1.0)


def evaluate_model(mod, A: float, B: float, phi_geom: float, phi_int: float):
    rows = []
    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    scale = 1.0 + lambda_univ

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        pred, residue, delta_geo, delta_spin = mod.predict_baryon(quarks, J)
        theta = mod.skew_angle(quarks)

        tri_geom = tri_wave(theta, phi_geom)
        vortex_int = 1.0 - abs(tri_wave(theta, phi_int))

        delta_geo_new = delta_geo + A * tri_geom + B * vortex_int
        pred_new = (pred - delta_geo + delta_geo_new) * scale

        err_pct = (pred_new - obs) / obs * 100.0
        abs_err_pct = abs(err_pct)

        rows.append({
            "name": name,
            "quarks": quarks,
            "obs": obs,
            "pred_new": pred_new,
            "err_pct": err_pct,
            "abs_err_pct": abs_err_pct,
            "theta": theta,
            "tri_geom": tri_geom,
            "vortex_int": vortex_int,
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
        "B": B,
        "phi_geom": phi_geom,
        "phi_int": phi_int,
        "rows": rows,
        "mape_all": mape_all,
        "mape_clean": mape_clean,
    }


def fit_best(mod, objective="all"):
    best = None

    # coarse search
    A_grid_1 = np.linspace(-30.0, 30.0, 61)
    B_grid_1 = np.linspace(-10.0, 10.0, 41)
    pg_grid_1 = np.linspace(45.0, 75.0, 61)
    pi_grid_1 = np.linspace(45.0, 65.0, 41)

    for A in A_grid_1:
        for B in B_grid_1:
            for phi_geom in pg_grid_1:
                for phi_int in pi_grid_1[::2]:
                    result = evaluate_model(mod, float(A), float(B), float(phi_geom), float(phi_int))
                    score = result["mape_clean"] if objective == "clean" else result["mape_all"]
                    if best is None or score < best["score"]:
                        best = {"score": score, **result}

    # refine around best
    A0 = best["A"]
    B0 = best["B"]
    pg0 = best["phi_geom"]
    pi0 = best["phi_int"]

    A_grid_2 = np.linspace(A0 - 5.0, A0 + 5.0, 81)
    B_grid_2 = np.linspace(B0 - 3.0, B0 + 3.0, 61)
    pg_grid_2 = np.linspace(pg0 - 4.0, pg0 + 4.0, 81)
    pi_grid_2 = np.linspace(pi0 - 4.0, pi0 + 4.0, 81)

    for A in A_grid_2[::2]:
        for B in B_grid_2[::2]:
            for phi_geom in pg_grid_2[::2]:
                for phi_int in pi_grid_2[::2]:
                    result = evaluate_model(mod, float(A), float(B), float(phi_geom), float(phi_int))
                    score = result["mape_clean"] if objective == "clean" else result["mape_all"]
                    if score < best["score"]:
                        best = {"score": score, **result}

    return best


def baseline(mod):
    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    scale = 1.0 + lambda_univ

    rows = []
    for name, quarks, J, obs, sector, note in mod.BARYONS:
        pred, residue, delta_geo, delta_spin = mod.predict_baryon(quarks, J)
        pred_scaled = pred * scale
        err_pct = (pred_scaled - obs) / obs * 100.0
        rows.append({
            "name": name,
            "err_pct": err_pct,
            "abs_err_pct": abs(err_pct),
        })

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}

    clean_rows = [r for r in rows if r["name"] not in charm_names and r["name"] not in omega_names]

    return {
        "all": float(np.mean([r["abs_err_pct"] for r in rows])),
        "clean": float(np.mean([r["abs_err_pct"] for r in clean_rows])),
        "rows": rows,
    }


def main():
    mod = load_module(BASE_FILE)
    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    base = baseline(mod)

    best_all = fit_best(mod, objective="all")
    best_clean = fit_best(mod, objective="clean")

    base_map = {r["name"]: r for r in base["rows"]}
    all_map = {r["name"]: r for r in best_all["rows"]}
    clean_map = {r["name"]: r for r in best_clean["rows"]}

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}

    lines = []
    lines.append("=" * 90)
    lines.append("BARYON DUAL-ANGLE VORTEX TEST")
    lines.append("=" * 90)
    lines.append("")
    lines.append(f"Base file:                  {BASE_FILE.name}")
    lines.append(f"lambda_univ:                {lambda_univ:.8f}")
    lines.append("")
    lines.append("Model:")
    lines.append("  tri_geom   = tri_wave(theta, phi_geom)")
    lines.append("  vortex_int = 1 - abs(tri_wave(theta, phi_int))")
    lines.append("  delta_geo_new = delta_geo + A * tri_geom + B * vortex_int")
    lines.append("  M_final = (M_geom - delta_geo + delta_geo_new) * (1 + lambda_univ)")
    lines.append("  theta = skew_angle(quarks) as current proxy")
    lines.append("")
    lines.append("Baseline (lambda_univ only):")
    lines.append(f"  all-set MAPE:             {base['all']:.4f}%")
    lines.append(f"  clean-set MAPE:           {base['clean']:.4f}%")
    lines.append("")
    lines.append("Best fit minimizing ALL set:")
    lines.append(f"  A:                        {best_all['A']:.6f}")
    lines.append(f"  B:                        {best_all['B']:.6f}")
    lines.append(f"  phi_geom:                 {best_all['phi_geom']:.6f} deg")
    lines.append(f"  phi_int:                  {best_all['phi_int']:.6f} deg")
    lines.append(f"  all-set MAPE:             {best_all['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:           {best_all['mape_clean']:.4f}%")
    lines.append("")
    lines.append("Best fit minimizing CLEAN set:")
    lines.append(f"  A:                        {best_clean['A']:.6f}")
    lines.append(f"  B:                        {best_clean['B']:.6f}")
    lines.append(f"  phi_geom:                 {best_clean['phi_geom']:.6f} deg")
    lines.append(f"  phi_int:                  {best_clean['phi_int']:.6f} deg")
    lines.append(f"  all-set MAPE:             {best_clean['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:           {best_clean['mape_clean']:.4f}%")
    lines.append("")
    lines.append("-" * 90)
    lines.append("Per-baryon comparison")
    lines.append("-" * 90)
    header = f"{'Baryon':<10} {'Base%':>9} {'AllFit%':>9} {'CleanFit%':>10}"
    lines.append(header)
    lines.append("-" * len(header))

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        b = base_map[name]["err_pct"]
        a = all_map[name]["err_pct"]
        c = clean_map[name]["err_pct"]
        tag = ""
        if name in omega_names:
            tag = " [omega]"
        elif name in charm_names:
            tag = " [charm]"
        lines.append(f"{name:<10} {b:>+9.3f} {a:>+9.3f} {c:>+10.3f}{tag}")

    lines.append("")
    lines.append("Notes:")
    lines.append("- clean set excludes Omega- and charm-sector baryons")
    lines.append("- phi_geom is the toroid/geometry angle")
    lines.append("- phi_int is the cancellation/vortex interaction angle")
    lines.append("- if phi_geom and phi_int split cleanly, that supports two distinct regimes")
    lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("")
    print(f"Saved report to: {REPORT_FILE}")


if __name__ == "__main__":
    main()