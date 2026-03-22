import numpy as np
from scipy.optimize import differential_evolution

# =============================================================================
# Mod-30 Spinor Geometry — Quark Mass Generation
# V9: V7 with charm chi=0 (balanced double vortex, beta handles crossover)
#
# Key insight: charm's -5.46% error in V3 was fixed in V7 not by the
# chirality sign but by the beta (non-Hilbert space) crossover correction.
# chi=+1 then overcorrected to +7.77%. Setting charm chi=0 lets beta
# do its job cleanly without chirality interference.
#
# Chirality assignments:
#   chi = +1   up, top       (C2 x C4 full positive winding)
#   chi = -1   down, strange, bottom  (C2 x C4 full negative winding)
#   chi =  0   charm         (Cycle 0: exactly balanced double vortex)
#
# Same 3 free parameters as V7 (alpha, gamma, beta).
# =============================================================================

LAMBDA_QCD = 217.0

current_masses = {
    'up':2.3, 'down':4.8, 'strange':95.0,
    'charm':1275.0, 'bottom':4180.0, 'top':173100.0
}
constituent_masses = {
    'up':336.0, 'down':340.0, 'strange':486.0,
    'charm':1550.0, 'bottom':4730.0, 'top':173400.0
}

quarks = ['up','down','strange','charm','bottom','top']
residues = [1,7,11,13,17,19,23,29]
angles_720 = {r: 2*360*r/30 for r in residues}
assignment = {'up':19,'down':11,'strange':7,'charm':23,'bottom':13,'top':17}

# chi=0 for charm: double vortex exactly balanced, beta handles crossover
chirality = {
    'up':+1.0, 'down':-1.0, 'strange':-1.0,
    'charm':0.0, 'bottom':-1.0, 'top':+1.0
}

def geo(t):
    return max(np.sin(np.radians(t)/2)**2, 1e-6)

def solve_v9(quark, res, alpha, gamma, beta, max_iter=300, tol=1e-7):
    t0  = angles_720[res]
    m_c = current_masses[quark]
    chi = chirality[quark]
    m   = m_c + alpha*LAMBDA_QCD/geo(t0)
    for _ in range(max_iter):
        x     = m/LAMBDA_QCD
        t_eff = t0 + chi*gamma*x*(1.0 - beta*x)*(180.0/np.pi)
        m_new = m_c + alpha*LAMBDA_QCD/geo(t_eff)
        if abs(m_new-m)/(abs(m)+1e-10) < tol:
            return m_new
        m = 0.6*m_new + 0.4*m
    return m

def mape_v9(params):
    alpha, gamma, beta = params
    if alpha <= 0: return 1e9
    return np.mean([
        abs(solve_v9(q,assignment[q],alpha,gamma,beta) - constituent_masses[q])
        / constituent_masses[q]
        for q in quarks
    ])*100

print("="*70)
print("Mod-30 V9 — charm chi=0, beta retained")
print("="*70)
print("\nOptimizing...")

result = differential_evolution(
    mape_v9,
    bounds=[(0.01,5.0),(-2.0,2.0),(0.0,0.1)],
    seed=42, maxiter=1000, tol=1e-10, popsize=30
)

alpha_opt, gamma_opt, beta_opt = result.x
x_cross = 1.0/beta_opt if beta_opt > 0 else float('inf')

print(f"\n  alpha = {alpha_opt:.5f}")
print(f"  gamma = {gamma_opt:.5f}")
print(f"  beta  = {beta_opt:.6f}")
print(f"  Crossover mass: {x_cross*LAMBDA_QCD:.1f} MeV")

print(f"\n{'Quark':>10}  {'Chi':>5}  {'Res':>4}  {'theta_0':>8}  {'theta_eff':>10}"
      f"  {'m_cur':>8}  {'m_QCD':>8}  {'m_V9':>8}  {'Error%':>8}")
print("-"*82)

predictions = {}
for q in quarks:
    r    = assignment[q]
    t0   = angles_720[r]
    chi  = chirality[q]
    m_c  = current_masses[q]
    m_q  = constituent_masses[q]
    m_v9 = solve_v9(q,r,alpha_opt,gamma_opt,beta_opt)
    x    = m_v9/LAMBDA_QCD
    t_eff = t0 + chi*gamma_opt*x*(1.0-beta_opt*x)*(180.0/np.pi)
    err  = (m_v9-m_q)/m_q*100
    predictions[q] = m_v9
    print(f"{q:>10}  {chi:>+5.1f}  {r:>4}  {t0:>7.1f}d  "
          f"{t_eff:>9.1f}d  {m_c:>8.1f}  {m_q:>8.1f}  {m_v9:>8.1f}  {err:>+8.2f}%")

errors_all = [abs(predictions[q]-constituent_masses[q])/constituent_masses[q]*100 for q in quarks]
errors_5   = [abs(predictions[q]-constituent_masses[q])/constituent_masses[q]*100 for q in quarks if q!='strange']
errors_up  = [abs(predictions[q]-constituent_masses[q])/constituent_masses[q]*100 for q in ['up','charm','top']]
errors_dn  = [abs(predictions[q]-constituent_masses[q])/constituent_masses[q]*100 for q in ['down','bottom']]
rmse_6     = np.sqrt(np.mean([(predictions[q]-constituent_masses[q])**2 for q in quarks]))

print(f"\n{'='*70}")
print(f"STATISTICS")
print(f"{'='*70}")
print(f"\n  Free parameters:  3  (alpha, gamma, beta)")
print(f"  Charm chirality:  0.0  (balanced double vortex)")
print(f"  Others:           +/-1.0  (C2 x C4 fixed by isospin)")
print(f"\n  6-quark MAPE:             {np.mean(errors_all):.4f}%")
print(f"  6-quark RMSE:             {rmse_6:.2f} MeV")
print(f"  5-quark MAPE (no strange):{np.mean(errors_5):.4f}%")
print(f"  Up-type   MAPE (u,c,t):   {np.mean(errors_up):.4f}%")
print(f"  Down-type MAPE (d,b):     {np.mean(errors_dn):.4f}%")
print(f"\n  V7 comparison:")
print(f"  V7:  charm chi=+1.0  →  6Q MAPE: 1.4100%,  charm error: +7.77%")
print(f"  V9:  charm chi= 0.0  →  6Q MAPE: {np.mean(errors_all):.4f}%,  charm error: {(predictions['charm']-constituent_masses['charm'])/constituent_masses['charm']*100:+.2f}%")
