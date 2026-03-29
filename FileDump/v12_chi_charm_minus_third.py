import numpy as np
from scipy.optimize import differential_evolution, minimize, minimize_scalar

# =============================================================================
# Mod-30 Spinor Geometry — V12
# Chi_charm derived from double helix helicity flip geometry
#
# Physical derivation:
#   - Charm is a double helix (forward + reverse winding, like geo_two)
#   - In a 720° spinor system, helicity flip occurs at 240° = 2/3 of cycle
#   - Charm starts with OPPOSITE chirality (-1, antimatter-oriented)
#   - Double helix helicity flip cancels 2/3 of that: -1 + 2/3 = -1/3
#   - Net chi_charm = -1/3 (matter side, suppressed coupling)
#   - This is NOT fitted — it is derived from the winding geometry
#
# V9 used chi_charm=0 (balanced double vortex argument) → ~7 MeV error on charm
# V12 uses chi_charm=-1/3 (helicity flip argument) → predicted to close the gap
#
# Two tests:
#   A) alpha FREE  (as in V9), chi_charm locked at -1/3
#   B) alpha LOCKED to IR fixed point 0.848809, chi_charm locked at -1/3
#
# Target: current quark masses (not constituent — constituent is emergent)
# =============================================================================

LAMBDA_QCD  = 217.0
ALPHA_IR    = 0.848809      # QCD IR fixed point
CHI_CHARM   = -1/3          # derived: -1 (opposite chirality) + 2/3 (helicity flip) = -1/3

current_masses = {
    'up':2.3, 'down':4.8, 'strange':95.0,
    'charm':1275.0, 'bottom':4180.0, 'top':173100.0
}
constituent_masses = {
    'up':336.0, 'down':340.0, 'strange':486.0,
    'charm':1550.0, 'bottom':4730.0, 'top':173400.0
}

quarks     = ['up','down','strange','charm','bottom','top']
angles_720 = {r: 2*360*r/30 for r in [1,7,11,13,17,19,23,29]}
assignment = {'up':19,'down':11,'strange':7,'charm':23,'bottom':13,'top':17}

chirality_v9  = {'up':+1.0,'down':-1.0,'strange':-1.0,'charm': 0.0,'bottom':-1.0,'top':+1.0}
chirality_v12 = {'up':+1.0,'down':-1.0,'strange':-1.0,'charm':-1/3,'bottom':-1.0,'top':+1.0}

def geo(t):
    return max(np.sin(np.radians(t)/2)**2, 1e-6)

def solve(quark, alpha, gamma, beta, chi_dict, max_iter=300, tol=1e-7):
    """Self-consistent mass solver.
    m = m_current + alpha*Λ/geo(t_eff)
    t_eff = t0 + chi*gamma*(m/Λ)*(1 - beta*(m/Λ)) * (180/pi)
    Targets constituent mass (emergent from iteration).
    """
    res = assignment[quark]
    t0  = angles_720[res]
    m_c = current_masses[quark]
    chi = chi_dict[quark]
    m   = m_c + alpha*LAMBDA_QCD/geo(t0)
    for _ in range(max_iter):
        x     = m/LAMBDA_QCD
        t_eff = t0 + chi*gamma*x*(1.0 - beta*x)*(180.0/np.pi)
        m_new = m_c + alpha*LAMBDA_QCD/geo(t_eff)
        if abs(m_new-m)/(abs(m)+1e-10) < tol:
            return m_new
        m = 0.6*m_new + 0.4*m
    return m

def run_model(alpha, gamma, beta, chi_dict, label):
    print(f"\n  {'Quark':<10} {'chi':>6}  {'target':>8}  {'pred':>8}  {'err%':>8}")
    print(f"  {'-'*52}")
    preds = {}
    for q in quarks:
        pred = solve(q, alpha, gamma, beta, chi_dict)
        tgt  = constituent_masses[q]
        preds[q] = pred
        print(f"  {q:<10} {chi_dict[q]:>+6.4f}  {tgt:>8.1f}  {pred:>8.1f}  {100*(pred-tgt)/tgt:>+8.3f}%")
    mape = np.mean([abs(preds[q]-constituent_masses[q])/constituent_masses[q] for q in quarks])*100
    charm_err = 100*(preds['charm']-constituent_masses['charm'])/constituent_masses['charm']
    print(f"\n  MAPE = {mape:.4f}%   charm_err = {charm_err:+.4f}%")
    return mape, preds

def optimize(alpha_fixed, chi_dict, label, alpha_bounds=None):
    print(f"\n{'='*65}")
    print(label)
    print("="*65)

    if alpha_fixed is not None:
        # alpha locked, optimize gamma + beta only
        def loss(p):
            g, b = p
            vals = [abs(solve(q,alpha_fixed,g,b,chi_dict)-constituent_masses[q])
                    /constituent_masses[q] for q in quarks]
            return np.mean(vals)*100
        res = differential_evolution(loss, bounds=[(-2.0,2.0),(0.0,0.1)],
                                     seed=42, maxiter=1000, tol=1e-11, popsize=25)
        res2 = minimize(loss, res.x, method='Nelder-Mead',
                        options={'xatol':1e-12,'fatol':1e-12,'maxiter':30000})
        best = res2 if res2.fun < res.fun else res
        g_opt, b_opt = best.x
        a_opt = alpha_fixed
    else:
        # alpha free, optimize alpha + gamma + beta
        def loss(p):
            a, g, b = p
            if a <= 0: return 1e9
            vals = [abs(solve(q,a,g,b,chi_dict)-constituent_masses[q])
                    /constituent_masses[q] for q in quarks]
            return np.mean(vals)*100
        res = differential_evolution(loss, bounds=[(0.01,5.0),(-2.0,2.0),(0.0,0.1)],
                                     seed=42, maxiter=1000, tol=1e-11, popsize=25)
        res2 = minimize(loss, res.x, method='Nelder-Mead',
                        options={'xatol':1e-12,'fatol':1e-12,'maxiter':30000})
        best = res2 if res2.fun < res.fun else res
        a_opt, g_opt, b_opt = best.x

    print(f"\n  alpha = {a_opt:.6f}{'  (locked to IR)' if alpha_fixed else '  (free)'}")
    print(f"  gamma = {g_opt:.6f}")
    print(f"  beta  = {b_opt:.6f}")
    print(f"  chi_charm = {chi_dict['charm']:+.6f}  ({chi_dict['charm']:+.10f})")
    mape, preds = run_model(a_opt, g_opt, b_opt, chi_dict, label)
    return a_opt, g_opt, b_opt, mape, preds

# =============================================================================
# TEST A: V9 baseline — alpha free, chi_charm = 0
# =============================================================================
a_v9, g_v9, b_v9, mape_v9, preds_v9 = optimize(
    alpha_fixed=None,
    chi_dict=chirality_v9,
    label="TEST A — V9 baseline: alpha FREE, chi_charm = 0"
)

# =============================================================================
# TEST B: V12a — alpha free, chi_charm = -1/3
# =============================================================================
a_b, g_b, b_b, mape_b, preds_b = optimize(
    alpha_fixed=None,
    chi_dict=chirality_v12,
    label="TEST B — V12a: alpha FREE, chi_charm = -1/3 (derived)"
)

# =============================================================================
# TEST C: V12b — alpha locked to IR, chi_charm = -1/3
# =============================================================================
a_c, g_c, b_c, mape_c, preds_c = optimize(
    alpha_fixed=ALPHA_IR,
    chi_dict=chirality_v12,
    label=f"TEST C — V12b: alpha LOCKED={ALPHA_IR} (IR fixed point), chi_charm = -1/3"
)

# =============================================================================
# TEST D: chi_charm sweep — find exact minimum, check if -1/3 is it
# (alpha free, gamma/beta re-optimized at each chi_charm)
# =============================================================================
print(f"\n{'='*65}")
print("TEST D — chi_charm sweep: does -1/3 land on the minimum?")
print("="*65)

def mape_for_chi(chi_c):
    chi_t = chirality_v9.copy(); chi_t['charm'] = chi_c
    def loss(p):
        a,g,b = p
        if a<=0: return 1e9
        return np.mean([abs(solve(q,a,g,b,chi_t)-constituent_masses[q])
                        /constituent_masses[q] for q in quarks])*100
    r = differential_evolution(loss, bounds=[(0.01,5.0),(-2.0,2.0),(0.0,0.1)],
                                seed=42, maxiter=300, tol=1e-9, popsize=15)
    return r.fun

sweep_vals = np.linspace(-0.8, 0.8, 33)   # coarse sweep first
print(f"\n  Coarse sweep (33 points, alpha re-optimized at each):")
print(f"  {'chi_charm':>10}  {'MAPE%':>8}")
sweep_mapes = []
for chi_c in sweep_vals:
    m = mape_for_chi(chi_c)
    sweep_mapes.append(m)
    marker = " <-- -1/3" if abs(chi_c+1/3)<0.04 else ""
    marker = " <-- 0   " if abs(chi_c)<0.04 else marker
    print(f"  {chi_c:>10.4f}  {m:>8.4f}{marker}")

best_idx = np.argmin(sweep_mapes)
print(f"\n  Sweep minimum at chi_charm = {sweep_vals[best_idx]:.4f}, MAPE = {sweep_mapes[best_idx]:.4f}%")
print(f"  -1/3 = {-1/3:.6f}")
print(f"  Distance from sweep min to -1/3: {abs(sweep_vals[best_idx]+1/3):.4f}")

# =============================================================================
# SUMMARY
# =============================================================================
print(f"\n{'='*65}")
print("SUMMARY")
print("="*65)
print(f"\n  {'Model':<45} {'MAPE%':>7}  {'charm err%':>10}")
print(f"  {'-'*65}")
charm_v9  = 100*(preds_v9['charm'] -constituent_masses['charm'])/constituent_masses['charm']
charm_b   = 100*(preds_b['charm']  -constituent_masses['charm'])/constituent_masses['charm']
charm_c   = 100*(preds_c['charm']  -constituent_masses['charm'])/constituent_masses['charm']
print(f"  {'A: V9   alpha free,   chi_charm=0':<45} {mape_v9:>7.4f}  {charm_v9:>+10.4f}%")
print(f"  {'B: V12a alpha free,   chi_charm=-1/3 (derived)':<45} {mape_b:>7.4f}  {charm_b:>+10.4f}%")
print(f"  {'C: V12b alpha=IR,     chi_charm=-1/3 (derived)':<45} {mape_c:>7.4f}  {charm_c:>+10.4f}%")
print(f"\n  Physical derivation of chi_charm=-1/3:")
print(f"    Charm = double helix, starts antimatter-oriented: chi = -1")
print(f"    720deg system helicity flip at 240deg = 2/3 of cycle")
print(f"    Flip cancels 2/3 of chi: -1 + 2/3 = -1/3")
print(f"    Net chi_charm = -1/3 (matter side, suppressed)")
print(f"\n  If sweep minimum (Test D) lands near -1/3:")
print(f"    → derivation confirmed, chi_charm is NOT a free parameter")
print(f"  If sweep minimum is elsewhere:")
print(f"    → helicity flip geometry needs revision")
