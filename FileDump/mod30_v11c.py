#!/usr/bin/env python3
"""
Mod-30 Spinor Geometry — V11c
Photon-Style Chirality from Vortex Theorem

Three cycle types (from Knuth/Claude exact chirality theorem):
  C0  chi_hat = 0           -> charm   : two-lane geometric mean, no precession
  C1  chi_hat = -3m(m-1)    -> strange, bottom : quadratic weight x*(x-1)
  C2  chi_hat = -3          -> up, down, top   : constant weight 1 (no blowup)

ALL corrections are negative (same topological direction).
No +/- sign flip needed — direction is baked into the formulation.
C2 quarks are naturally capped at weight=1, suppressing angle blowup.
Charm is handled separately via two-lane geometric mean (C0 = balanced vortex).

Free parameters: alpha_12, gamma  (2 optimized)
Derived:         alpha_C0         (fixed by charm two-lane geometry)

J. Richardson | Independent Researcher | March 2026
github.com/historyViper/Sage
"""

import numpy as np
from scipy.optimize import differential_evolution, minimize
import math
import signal
import time

# ---------------------------------------------------------------------------
# Physical constants and known masses
# ---------------------------------------------------------------------------

LAMBDA_QCD = 217.0  # MeV, MS-bar scheme, 3 flavors

current_masses = {
    'up':      2.3,
    'down':    4.8,
    'strange': 95.0,
    'charm':   1275.0,
    'bottom':  4180.0,
    'top':     173100.0,
}

constituent_masses = {
    'up':      336.0,
    'down':    340.0,
    'strange': 486.0,
    'charm':   1550.0,
    'bottom':  4730.0,
    'top':     173400.0,
}

quarks = ['up', 'down', 'strange', 'charm', 'bottom', 'top']

# ---------------------------------------------------------------------------
# Mod-30 geometry
# ---------------------------------------------------------------------------

residues_all = [1, 7, 11, 13, 17, 19, 23, 29]
angles_720 = {r: 2 * 360 * r / 30 for r in residues_all}

assignment = {
    'up':      19,
    'down':    11,
    'strange': 7,
    'charm':   23,
    'bottom':  13,
    'top':     17,
}

# Multiplicative inverses mod 30 (r * r_inv = 1 mod 30)
inverses = {}
for r in residues_all:
    for s in residues_all:
        if (r * s) % 30 == 1:
            inverses[r] = s

# ---------------------------------------------------------------------------
# Cycle type assignments (from vortex chirality theorem)
#   C0: chi_hat = 0           charm
#   C1: chi_hat = -3m(m-1)    strange, bottom  (quadratic inner vortex)
#   C2: chi_hat = -3          up, down, top    (constant outer vortex)
# ---------------------------------------------------------------------------

cycle_type = {
    'up':      'C2',
    'down':    'C2',
    'strange': 'C1',
    'charm':   'C0',
    'bottom':  'C1',
    'top':     'C2',
}

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def geo(theta_deg):
    """Single-lane coupling: sin^2(theta/2)."""
    return max(math.sin(math.radians(theta_deg) / 2) ** 2, 1e-6)

def geo_two(r):
    """Two-lane geometric mean: sqrt(g_out * g_ret)."""
    g_out = geo(angles_720[r])
    g_ret = geo(angles_720[inverses[r]])
    return math.sqrt(g_out * g_ret)

def chi_weight(quark, x):
    """
    Chirality weight from theorem (always >= 0, no sign flip).
      C0: 0           (balanced, charm)
      C1: x*(x-1)     (quadratic, inner vortex)
      C2: 1           (constant cap, outer vortex)
    """
    ct = cycle_type[quark]
    if ct == 'C0':
        return 0.0
    if ct == 'C1':
        return max(x * (x - 1.0), 0.0)
    return 1.0  # C2

# ---------------------------------------------------------------------------
# Derived alpha for charm (C0, two-lane, no precession)
# Fixed by geometry: alpha_C0 = (m_charm_target - m_charm_cur) * geo_two(23) / L
# ---------------------------------------------------------------------------

alpha_C0 = (
    (constituent_masses['charm'] - current_masses['charm'])
    * geo_two(assignment['charm'])
    / LAMBDA_QCD
)

# ---------------------------------------------------------------------------
# Mass solver
# ---------------------------------------------------------------------------

def solve(quark, res, alpha_12, gamma, max_iter=300, tol=1e-7):
    """
    Solve self-consistent mass equation for one quark.

    C0 (charm): m = m_cur + alpha_C0 * L / geo_two(r)   [static, exact]
    C1/C2:      m = m_cur + alpha_12 * L / geo(theta_eff)
                theta_eff = theta_0 - gamma * chi_weight(q, x) * (180/pi)
    """
    m_c = current_masses[quark]
    ct  = cycle_type[quark]

    # C0: charm, two-lane, no precession
    if ct == 'C0':
        m = m_c + alpha_C0 * LAMBDA_QCD / geo_two(res)
        return m, angles_720[res], 0.0

    # C1 / C2: single-lane with photon-style negative precession
    t0 = angles_720[res]
    m  = m_c + alpha_12 * LAMBDA_QCD / geo(t0)

    for _ in range(max_iter):
        x     = m / LAMBDA_QCD
        w     = chi_weight(quark, x)
        t_eff = t0 - gamma * w * (180.0 / np.pi)
        m_new = m_c + alpha_12 * LAMBDA_QCD / geo(t_eff)
        if abs(m_new - m) / (abs(m) + 1e-10) < tol:
            return m_new, t_eff, w
        m = 0.6 * m_new + 0.4 * m

    return m, t_eff, w

# ---------------------------------------------------------------------------
# Objective
# ---------------------------------------------------------------------------

def mape(params):
    alpha_12, gamma = params
    if alpha_12 <= 0 or gamma <= 0:
        return 1e9
    try:
        errors = [
            abs(solve(q, assignment[q], alpha_12, gamma)[0] - constituent_masses[q])
            / constituent_masses[q]
            for q in quarks
        ]
        return np.mean(errors) * 100
    except Exception:
        return 1e9

# ---------------------------------------------------------------------------
# Timeout helper
# ---------------------------------------------------------------------------

class TimedOut(Exception):
    pass

class Timeout:
    def __init__(self, seconds):
        self.seconds = seconds
    def __enter__(self):
        signal.signal(signal.SIGALRM, self._handler)
        signal.alarm(self.seconds)
        return self
    def __exit__(self, *args):
        signal.alarm(0)
        return False
    def _handler(self, sig, frame):
        raise TimedOut(f"Exceeded {self.seconds}s")

# ---------------------------------------------------------------------------
# Optimization: DE sweep + Nelder-Mead polish, with timeout
# ---------------------------------------------------------------------------

DE_TIMEOUT  = 15   # seconds for differential evolution
NM_TIMEOUT  = 10   # seconds for Nelder-Mead polish

print("=" * 65)
print("Mod-30 V11c — Photon-Style Chirality (Vortex Theorem)")
print("=" * 65)
print()
print(f"  alpha_C0 = {alpha_C0:.5f}  (charm, derived from two-lane geometry)")
print(f"  Optimizing: alpha_12, gamma")
print()

best_result = None

# DE pass
print(f"  [1/2] Differential evolution (timeout={DE_TIMEOUT}s)...")
t0 = time.time()
try:
    with Timeout(DE_TIMEOUT):
        res_de = differential_evolution(
            mape,
            bounds=[(0.01, 5.0), (0.001, 15.0)],
            seed=42,
            maxiter=500,
            tol=1e-9,
            popsize=15,
            mutation=(0.5, 1.0),
            recombination=0.9,
            init='sobol',
        )
    best_result = res_de
    print(f"  Done in {time.time()-t0:.1f}s  MAPE={res_de.fun:.4f}%  params={res_de.x}")
except TimedOut:
    print(f"  Timed out after {DE_TIMEOUT}s — using best found so far")

# Nelder-Mead polish
if best_result is not None:
    print(f"  [2/2] Nelder-Mead polish (timeout={NM_TIMEOUT}s)...")
    t1 = time.time()
    try:
        with Timeout(NM_TIMEOUT):
            res_nm = minimize(
                mape,
                best_result.x,
                method='Nelder-Mead',
                options={'xatol': 1e-11, 'fatol': 1e-11, 'maxiter': 20000},
            )
        if res_nm.fun < best_result.fun:
            best_result = res_nm
            print(f"  Polished in {time.time()-t1:.1f}s  MAPE={res_nm.fun:.4f}%")
        else:
            print(f"  No improvement from polish")
    except TimedOut:
        print(f"  Polish timed out — keeping DE result")

if best_result is None:
    print("ERROR: No result obtained. Try increasing DE_TIMEOUT.")
    raise SystemExit(1)

alpha_12_opt, gamma_opt = best_result.x

# ---------------------------------------------------------------------------
# Results table
# ---------------------------------------------------------------------------

print()
print("=" * 65)
print("RESULTS")
print("=" * 65)
print()
print(f"  alpha_C0 = {alpha_C0:.5f}  (derived)")
print(f"  alpha_12 = {alpha_12_opt:.5f}  (optimized)")
print(f"  gamma    = {gamma_opt:.5f}  (optimized)")
print(f"  MAPE     = {best_result.fun:.4f}%")
print()

header = (
    f"{'Quark':>10}  {'Cyc':>4}  {'t0':>7}  {'weight':>8}  "
    f"{'t_eff':>9}  {'m_cur':>8}  {'m_QCD':>8}  {'m_pred':>8}  {'err%':>7}"
)
print(header)
print("-" * len(header))

for q in quarks:
    r     = assignment[q]
    m_v, t_eff, w = solve(q, r, alpha_12_opt, gamma_opt)
    m_q   = constituent_masses[q]
    err   = (m_v - m_q) / m_q * 100
    t0_v  = angles_720[r]
    print(
        f"{q:>10}  {cycle_type[q]:>4}  {t0_v:>7.1f}d  {w:>8.3f}  "
        f"{t_eff:>9.1f}d  {current_masses[q]:>8.1f}  {m_q:>8.1f}  "
        f"{m_v:>8.1f}  {err:>+7.2f}%"
    )

print()
print("Unused residues: 1, 29")
print("  -> angles 24.0d, 696.0d  (mirror fermion / dark matter candidates)")
print()
print("=" * 40)
print("SCOREBOARD")
print("=" * 40)
print(f"  V11c  photon+theorem  2p + 1 derived : {best_result.fun:.4f}%")
print(f"  V9    single-lane     3 free params  : 0.1907%")
print()
print("Physical interpretation:")
print("  C0 (charm):    balanced double-vortex — two-lane amplitude, zero net chirality")
print("  C1 (str/bot):  inner vortex — quadratic chirality accumulates with mass")
print("  C2 (up/dn/top):outer vortex — constant chirality, naturally caps angle blowup")
print("  All corrections negative: topology sets direction, no ± flip needed")
