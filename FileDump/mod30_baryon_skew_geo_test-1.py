#!/usr/bin/env python3
"""
mod30_baryon_skew_geo_test.py

Diagnostic extension of mod30_complete_v2.py

Tests two ways of inserting skew inside the geometric term:

1) additive:
   delta_geo_new = delta_geo + eps * (skew / 240)

2) multiplicative:
   delta_geo_new = delta_geo * (1 + eps * (skew / 240))

Then applies the universal boundary factor:

   lambda_univ = GEO_BOUNDARY / ALPHA_QUARK
   M_final = M_geom_modified * (1 + lambda_univ)

Outputs:
- best-fit eps for additive and multiplicative versions
- all-set and clean-set MAPE
- per-baryon comparison table
- text report saved to /mnt/data
"""

import importlib.util
from pathlib import Path
import numpy as np

BASE_FILE = Path("/mnt/data/mod30_complete_v2.py")
REPORT_FILE = Path("/mnt/data/mod30_baryon_skew_geo_test_report.txt")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("mod30_complete_v2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def evaluate_model(mod, eps: float, mode: str):
    rows = []

    lambda_univ = mod.GEO_BOUNDARY / mod.ALPHA_QUARK
    scale = 1.0 + lambda_univ

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        pred, residue, delta_geo, delta_spin = mod.predict_baryon(quarks, J)
        skew = mod.skew_angle(quarks)
        skew_norm = skew / 240.0

        if mode == "additive":
            delta_geo_new = delta_geo + eps * skew_norm
        elif mode == "multiplicative":
            delta_geo_new = delta_geo * (1.0 + eps * skew_norm)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        pred_new = (pred - delta_geo + delta_geo_new) * scale
        err_pct = (pred_new - obs) / obs * 100.0
        abs_err_pct = abs(err_pct)

        rows.append({
            "name": name,
            "obs": obs,
            "pred_new": pred_new,
            "err_pct": err_pct,
            "abs_err_pct": abs_err_pct,
            "skew": skew,
            "sector": sector,
            "note": note,
        })

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}
    clean_rows = [r for r in rows if r["name"] not in charm_names and r["name"] not in omega_names]

    mape_all = float(np.mean([r["abs_err_pct"] for r in rows]))
    mape_clean = float(np.mean([r["abs_err_pct"] for r in clean_rows]))

    return {
        "eps": eps,
        "mode": mode,
        "rows": rows,
        "mape_all": mape_all,
        "mape_clean": mape_clean,
    }


def fit_best_eps(mod, mode: str, eps_min=-10.0, eps_max=10.0, n=4001):
    best = None
    for eps in np.linspace(eps_min, eps_max, n):
        result = evaluate_model(mod, float(eps), mode)
        if best is None or result["mape_all"] < best["mape_all"]:
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
            "pred_new": pred_scaled,
            "err_pct": err_pct,
            "abs_err_pct": abs(err_pct),
            "sector": sector,
            "note": note,
        })

    charm_names = {"Lambda_c", "Omega_c", "Xi_cc++", "Xi_cc+"}
    omega_names = {"Omega-"}
    baseline_clean = [r for r in baseline_rows if r["name"] not in charm_names and r["name"] not in omega_names]
    baseline_mape_all = float(np.mean([r["abs_err_pct"] for r in baseline_rows]))
    baseline_mape_clean = float(np.mean([r["abs_err_pct"] for r in baseline_clean]))

    best_add = fit_best_eps(mod, "additive")
    best_mul = fit_best_eps(mod, "multiplicative")

    lines = []
    lines.append("=" * 80)
    lines.append("BARYON SKEW-IN-GEOMETRY TEST")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Base file:               {BASE_FILE.name}")
    lines.append(f"lambda_univ:             {lambda_univ:.8f}")
    lines.append(f"scale factor:            {scale:.8f}")
    lines.append("")
    lines.append("Baseline (universal factor only):")
    lines.append(f"  all-set MAPE:          {baseline_mape_all:.4f}%")
    lines.append(f"  clean-set MAPE:        {baseline_mape_clean:.4f}%")
    lines.append("")
    lines.append("Best additive skew-in-geometry:")
    lines.append(f"  equation:              delta_geo_new = delta_geo + eps * (skew/240)")
    lines.append(f"  best eps:              {best_add['eps']:.6f}")
    lines.append(f"  all-set MAPE:          {best_add['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:        {best_add['mape_clean']:.4f}%")
    lines.append("")
    lines.append("Best multiplicative skew-in-geometry:")
    lines.append(f"  equation:              delta_geo_new = delta_geo * (1 + eps * (skew/240))")
    lines.append(f"  best eps:              {best_mul['eps']:.6f}")
    lines.append(f"  all-set MAPE:          {best_mul['mape_all']:.4f}%")
    lines.append(f"  clean-set MAPE:        {best_mul['mape_clean']:.4f}%")
    lines.append("")

    lines.append("-" * 80)
    lines.append("Per-baryon comparison")
    lines.append("-" * 80)
    header = f"{'Baryon':<10} {'Obs':>10} {'Base%':>8} {'Add%':>8} {'Mul%':>8}"
    lines.append(header)
    lines.append("-" * len(header))

    add_map = {r["name"]: r for r in best_add["rows"]}
    mul_map = {r["name"]: r for r in best_mul["rows"]}
    base_map = {r["name"]: r for r in baseline_rows}

    for name, quarks, J, obs, sector, note in mod.BARYONS:
        base_err = base_map[name]["err_pct"]
        add_err = add_map[name]["err_pct"]
        mul_err = mul_map[name]["err_pct"]
        tag = ""
        if name in omega_names:
            tag = " [omega]"
        elif name in charm_names:
            tag = " [charm]"
        lines.append(f"{name:<10} {obs:>10.3f} {base_err:>+8.3f} {add_err:>+8.3f} {mul_err:>+8.3f}{tag}")

    lines.append("")
    lines.append("Notes:")
    lines.append("- clean set excludes Omega- and charm-sector baryons")
    lines.append("- additive and multiplicative versions both place skew inside geometry")
    lines.append("- if additive beats multiplicative on the clean set, that supports an inserted geometric term")
    lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("")
    print(f"Saved report to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
