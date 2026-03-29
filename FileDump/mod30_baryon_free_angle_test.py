#!/usr/bin/env python3
"""
mod30_baryon_free_angle_test.py

Diagnostic extension of mod30_complete_v2.py

Fits a local triangle-wave correction with a FREE angle parameter:

    delta_geo_new = delta_geo + A * tri_wave(theta, phi)

Then applies the universal boundary factor:

    lambda_univ = GEO_BOUNDARY / ALPHA_QUARK
    M_final = (M_geom - delta_geo + delta_geo_new) * (1 + lambda_univ)

Current proxy:
    theta = skew_angle(quarks)

The purpose is to let the data return the preferred local phase angle phi
instead of forcing 30 deg or 60 deg in advance.
"""

import importlib.util
from pathlib import Path
import numpy as np

BASE_FILE = Path("/mnt/data/mod30_complete_v2.py")
REPORT_FILE = Path("/mnt/data/mod30_baryon_free_angle_test_report.txt")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("mod30_complete_v2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tri_wave(theta_deg: float, segment_deg: float) -> float:
    x = (theta_deg / segment_deg) % 2.0
    return 1.0 - 2.0 * abs(x - 1.0)


def evaluate_model(mod, A: float, phi: float):
    rows = []
    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    scale = 1.0 + lambda_univ

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        pred, residue, delta_geo, delta_spin = mod.predict_baryon(quarks, J)
        theta = mod.skew_angle(quarks)
        tri = tri_wave(theta, phi)
        delta_geo_new = delta_geo + A * tri
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
            "tri": tri,
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
        "phi": phi,
        "rows": rows,
        "mape_all": mape_all,
        "mape_clean": mape_clean,
    }


def fit_best(mod, objective="clean"):
    best = None

    A_grid_1 = np.linspace(-20.0, 20.0, 201)
    phi_grid_1 = np.linspace(10.0, 120.0, 111)

    for A in A_grid_1:
        for phi in phi_grid_1:
            result = evaluate_model(mod, float(A), float(phi))
            score = result["mape_clean"] if objective == "clean" else result["mape_all"]
            if best is None or score < best["score"]:
                best = {"score": score, **result}

    A0 = best["A"]
    p0 = best["phi"]
    A_grid_2 = np.linspace(A0 - 2.0, A0 + 2.0, 201)
    phi_grid_2 = np.linspace(max(5.0, p0 - 6.0), min(150.0, p0 + 6.0), 241)

    for A in A_grid_2:
        for phi in phi_grid_2:
            result = evaluate_model(mod, float(A), float(phi))
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
    best_clean = fit_best(mod, objective="clean")
    best_all = fit_best(mod, objective="all")

    base_map = {r["name"]: r for r in base["rows"]}
    clean_map = {r["name"]: r for r in best_clean["rows"]}
    all_map = {r["name"]: r for r in best_all["rows"]}

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}

    lines = []
    lines.append("=" * 86)
    lines.append("BARYON FREE-ANGLE TRIANGLE-WAVE TEST")
    lines.append("=" * 86)
    lines.append("")
    lines.append(f"Base file:                 {BASE_FILE.name}")
    lines.append(f"lambda_univ:               {lambda_univ:.8f}")
    lines.append("")
    lines.append("Model:")
    lines.append("  delta_geo_new = delta_geo + A * tri_wave(theta, phi)")
    lines.append("  M_final = (M_geom - delta_geo + delta_geo_new) * (1 + lambda_univ)")
    lines.append("  theta = skew_angle(quarks) as current proxy")
    lines.append("")
    lines.append("Baseline (lambda_univ only):")
    lines.append(f"  all-set MAPE:            {base['all']:.4f}%")
    lines.append(f"  clean-set MAPE:          {base['clean']:.4f}%")
    lines.append("")
    lines.append("Best fit minimizing CLEAN set:")
    lines.append(f"  A:                       {best_clean['A']:.6f}")
    lines.append(f"  phi:                     {best_clean['phi']:.6f} deg")
    lines.append(f"  all-set MAPE:            {best_clean['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:          {best_clean['mape_clean']:.4f}%")
    lines.append("")
    lines.append("Best fit minimizing ALL set:")
    lines.append(f"  A:                       {best_all['A']:.6f}")
    lines.append(f"  phi:                     {best_all['phi']:.6f} deg")
    lines.append(f"  all-set MAPE:            {best_all['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:          {best_all['mape_clean']:.4f}%")
    lines.append("")
    lines.append("-" * 86)
    lines.append("Per-baryon comparison")
    lines.append("-" * 86)
    header = f"{'Baryon':<10} {'Base%':>9} {'CleanFit%':>10} {'AllFit%':>9}"
    lines.append(header)
    lines.append("-" * len(header))

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        b = base_map[name]["err_pct"]
        c = clean_map[name]["err_pct"]
        a = all_map[name]["err_pct"]
        tag = ""
        if name in omega_names:
            tag = " [omega]"
        elif name in charm_names:
            tag = " [charm]"
        lines.append(f"{name:<10} {b:>+9.3f} {c:>+10.3f} {a:>+9.3f}{tag}")

    lines.append("")
    lines.append("Notes:")
    lines.append("- clean set excludes Omega- and charm-sector baryons")
    lines.append("- if phi returns near 30 deg, that supports the normal-toroid / Hamiltonian picture")
    lines.append("- if phi returns near 60 deg, that supports the triangle-toroid picture")
    lines.append("- if phi returns elsewhere, the geometry may be mixed or projected")
    lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("")
    print(f"Saved report to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
