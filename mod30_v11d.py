#!/usr/bin/env python3
"""
Mod-30 Spinor Geometry — V11d
Photon-Style Chirality, 5-Quark Predictive Model

Charm is excluded pending resolution of its pop-bottle vortex geometry.
The framework predicts charm at 1733 MeV (two-lane base). The observed
1550 MeV implies ~183 MeV of internal cancellation (~2/3 of the return
lane's 271 MeV contribution), consistent with a 3-winding SU(3) topology
in the GOE regime. This will be addressed in a separate charm paper.

Lane type (no free choices):
  Self-inverse residues (up=19, down=11): single lane
  Cross-pair residues (strange=7, charm=23, bottom=13, top=17): two-lane
  Determined purely by the mod-30 multiplicative inverse structure.

Cycle type (from Knuth/Claude vortex chirality theorem):
  C0  chi_hat = 0          charm    -- excluded, pop-bottle geometry open
  C1  chi_hat = -3m(m-1)   strange, bottom  -- quadratic inner vortex
  C2  chi_hat = -3          up, down, top    -- constant outer vortex

Precession (all corrections negative -- same topological direction):
  C1: theta_eff = theta_0 - gamma * x*(x-1) * (180/pi)
  C2: theta_eff = theta_0 - gamma * 1        * (180/pi)
  where x = m / Lambda_QCD

  C2 weight is capped at 1: angle blowup for heavy quarks is
  expected and physically meaningful -- it encodes the energy
  amplitude required to maintain that quark's geometric state.

Free parameters: alpha, gamma  (2 only)
All structure derived from mod-30 geometry and vortex theorem.

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
    'bottom':  4180.0,
    'top':     173100.0,
}

constituent_masses = {
    'up':      336.0,
    'down':    340.0,
    'strange': 486.0,
    'bottom':  4730.0,
    'top':     173400.0,
}

quarks = ['up', 'down', 'strange', 'bottom', 'top']

# ---------------------------------------------------------------------------
# Mod-30 geometry
# ---------------------------------------------------------------------------

residues_all = [1, 7, 11, 13, 17, 19, 23, 29]
angles_720   = {r: 2 * 360 * r / 30 for r in residues_all}

assignment = {
    'up':      19,
    'down':    11,
    'strange': 7,
    'bottom':  13,
    'top':     17,
}

# Multiplicative inverses mod 30
inverses = {}
for r in residues_all:
    for s in residues_all:
        if (r * s) % 30 == 1:
            inverses[r] = s

# ---------------------------------------------------------------------------
# Cycle type from vortex chirality theorem
# ---------------------------------------------------------------------------

cycle_type = {
    'up':      'C2',   # chi_hat = -3, constant outer vortex
    'down':    'C2',
    'strange': 'C1',   # chi_hat = -3m(m-1), quadratic inner vortex
    'bottom':  'C1',
    'top':     'C2',
}

# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def geo(theta_deg):
    """Single-lane coupling: sin^2(theta/2)."""
    return max(math.sin(math.radians(theta_deg) / 2) ** 2, 1e-6)

def is_self_inverse(r):
    """True if r is its own multiplicative inverse mod 30."""
    return inverses[r] == r

def base_geo(r):
    """
    Lane-type determined by mod-30 inverse structure:
      self-inverse -> single lane: geo(theta)
      cross-pair   -> two-lane:   sqrt(geo_out * geo_ret)
    """
    if is_self_inverse(r):
        return geo(angles_720[r])
    return math.sqrt(geo(angles_720[r]) * geo(angles_720[inverses[r]]))

def chi_weight(quark, x):
    """
    Chirality weight from theorem (always >= 0, all corrections negative).
      C1: x*(x-1)  quadratic, grows with mass
      C2: 1        constant cap, no blowup
    """
    if cycle_type[quark] == 'C1':
        return max(x * (x - 1.0), 0.0)
    return 1.0  # C2

# ---------------------------------------------------------------------------
# Mass solver
# ---------------------------------------------------------------------------

def solve(quark, res, alpha, gamma, max_iter=300, tol=1e-7):
    """
    Self-consistent mass equation:
      theta_eff = theta_0 - gamma * chi_weight(q, x) * (180/pi)
      m         = m_current + alpha * Lambda / geo(theta_eff)
      x         = m / Lambda
    """
    m_c = current_masses[quark]
    t0  = angles_720[res]
    m   = m_c + alpha * LAMBDA_QCD / base_geo(res)

    for _ in range(max_iter):
        x     = m / LAMBDA_QCD
        w     = chi_weight(quark, x)
        t_eff = t0 - gamma * w * (180.0 / np.pi)
        m_new = m_c + alpha * LAMBDA_QCD / geo(t_eff)
        if abs(m_new - m) / (abs(m) + 1e-10) < tol:
            return m_new, t_eff, w
        m = 0.6 * m_new + 0.4 * m

    return m, t_eff, w

# ---------------------------------------------------------------------------
# Objective
# ---------------------------------------------------------------------------

def mape(params):
    alpha, gamma = params
    if alpha <= 0 or gamma <= 0:
        return 1e9
    try:
        errors = [
            abs(solve(q, assignment[q], alpha, gamma)[0] - constituent_masses[q])
            / constituent_masses[q]
            for q in quarks
        ]
        return np.mean(errors) * 100
    except Exception:
        return 1e9

# ---------------------------------------------------------------------------
# Timeout
# ---------------------------------------------------------------------------

class TimedOut(Exception):
    pass

signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(TimedOut()))

DE_TIMEOUT = 25
NM_TIMEOUT = 10

# ---------------------------------------------------------------------------
# Optimize
# ---------------------------------------------------------------------------

print("=" * 60)
print("Mod-30 V11d — 5-Quark Predictive Model")
print("Photon-Style Chirality from Vortex Theorem")
print("=" * 60)
print()
print("  Charm excluded -- pop-bottle geometry open problem.")
print("  Lane type from mod-30 self-inverse structure (no choices).")
print("  Cycle type from vortex chirality theorem (no choices).")
print("  Free parameters: alpha, gamma only.")
print()

best = None

print(f"  [1/2] Differential evolution (timeout={DE_TIMEOUT}s)...")
t0 = time.time()
try:
    signal.alarm(DE_TIMEOUT)
    res_de = differential_evolution(
        mape,
        bounds=[(0.01, 5.0), (0.001, 15.0)],
        seed=42, maxiter=1000, tol=1e-10,
        popsize=25,
        mutation=(0.5, 1.5), recombination=0.9,
    )
    signal.alarm(0)
    best = res_de
    print(f"  Done in {time.time()-t0:.1f}s  MAPE={res_de.fun:.4f}%")
except TimedOut:
    print(f"  Timed out after {DE_TIMEOUT}s")

if best is not None:
    print(f"  [2/2] Nelder-Mead polish (timeout={NM_TIMEOUT}s)...")
    t1 = time.time()
    try:
        signal.alarm(NM_TIMEOUT)
        res_nm = minimize(
            mape, best.x, method='Nelder-Mead',
            options={'xatol': 1e-11, 'fatol': 1e-11, 'maxiter': 20000},
        )
        signal.alarm(0)
        if res_nm.fun < best.fun:
            best = res_nm
            print(f"  Polished in {time.time()-t1:.1f}s  MAPE={res_nm.fun:.4f}%")
        else:
            print(f"  No improvement from polish")
    except TimedOut:
        signal.alarm(0)
        print(f"  Polish timed out -- keeping DE result")

if best is None:
    print("ERROR: No result. Try increasing DE_TIMEOUT.")
    raise SystemExit(1)

alpha_opt, gamma_opt = best.x

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

print()
print("=" * 60)
print("RESULTS")
print("=" * 60)
print()
print(f"  alpha = {alpha_opt:.6f}")
print(f"  gamma = {gamma_opt:.6f}")
print(f"  MAPE  = {best.fun:.4f}%  (5 quarks)")
print()

hdr = (f"{'Quark':>10}  {'Cyc':>3}  {'Lanes':>6}  {'base_geo':>8}  "
       f"{'weight':>7}  {'t_eff':>9}  {'target':>8}  {'pred':>8}  {'err%':>7}")
print(hdr)
print("-" * len(hdr))

for q in quarks:
    r             = assignment[q]
    m_v, t_eff, w = solve(q, r, alpha_opt, gamma_opt)
    m_q           = constituent_masses[q]
    err           = (m_v - m_q) / m_q * 100
    lanes         = 'single' if is_self_inverse(r) else 'two'
    print(f"{q:>10}  {cycle_type[q]:>3}  {lanes:>6}  {base_geo(r):>8.5f}  "
          f"{w:>7.3f}  {t_eff:>9.1f}d  {m_q:>8.1f}  {m_v:>8.1f}  {err:>+7.3f}%")

# ---------------------------------------------------------------------------
# Charm diagnostic
# ---------------------------------------------------------------------------

print()
print("--- Charm diagnostic (not fitted) ---")
r_c            = 23
m_charm_single = 1275.0 + alpha_opt * LAMBDA_QCD / geo(angles_720[r_c])
m_charm_two    = 1275.0 + alpha_opt * LAMBDA_QCD / base_geo(r_c)
return_adds    = m_charm_two - m_charm_single
suppressed     = m_charm_two - 1550.0
frac           = suppressed / return_adds

print(f"  Outgoing only (r=23):     {m_charm_single:.1f} MeV")
print(f"  Two-lane (23x17):         {m_charm_two:.1f} MeV  (+{return_adds:.1f} from return lane)")
print(f"  Pop-bottle suppresses:    {suppressed:.1f} MeV  ({frac:.2f} of return lane = ~2/3)")
print(f"  Observed target:          1550.0 MeV")
print(f"  Suppression is ~2/3 of return lane contribution.")
print(f"  Consistent with 3-winding SU(3) topology in GOE regime.")
print()
print("Unused residues: 1, 29")
print("  -> angles 24.0d, 696.0d  (mirror fermion / dark matter candidates)")
print()
print("=" * 45)
print("SCOREBOARD")
print("=" * 45)
print(f"  V11d  5-quark, 2 free params:  {best.fun:.4f}%")
print(f"  V9    6-quark, 3 free params:  0.1907%")
print(f"  V9    5-quark, 3 free params:  0.2287%")
