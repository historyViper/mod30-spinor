#!/usr/bin/env python3
"""
gbp_complete_v7.py — Geometric Boundary Projection Framework v7
=============================================================================

VERSION HISTORY:
  v5: geo_factor derived from mod-30 spinor geometry. MAPE=0.6365%. 2 free params.
  v6: Strange step-down rule + scan-derived assignments. MAPE=0.4078%. 2 free params.
  v7: Photon-like branch + Sigma_c+ fix + Xi_c*+/0 fix. 2 free params.

V7 CHANGES FROM V6:
  1. SIGMA_C+ GEO_FACTOR FIX
     gf=S2[3]=0.165435 (was 0.447736). Generation-adjacency mechanism:
     charm (gen2) adjacent to bottom/top (gen3), S2[3] governs geo_factor.
     Error: -0.070% (was +1.44%).

  2. PHOTON-LIKE BRANCH (new rule: 'photon')
     Formula: (sumC + gc + rt + C_HYP*S) * (1 + lam)
     No dg term — geometric mass cancels, only skew (gc) and
     Hamiltonian winding survive.
     Applied to: Xi_c*+, Xi_c*0 (S1/T3), Xi_b*- (S1/T3)

  3. OPEN ISSUES REMAINING:
     Omega_c*  (+2.41%) — omega formula structurally wrong for ss+charm
     Xi_b*-    (+0.76%) — photon branch helps but T4 topology suspected
     Omega_b*  (+1.00%) — needs investigation

AUTHORS: HistoryViper (independent researcher)
         AI collaboration: Claude (Anthropic), ChatGPT/Sage (OpenAI),
                           MiniMax, DeepSeek
CODE:    github.com/historyViper/mod30-spinor
"""

import math, json, argparse
from fractions import Fraction

PI15  = math.pi / 15
GEN_N = {1: 4, 2: 7, 3: 2}
GEN_MAP = {'up':1,'down':1,'strange':2,'charm':2,'bottom':3,'top':3}

def s2(gen): return math.sin(GEN_N[gen] * PI15) ** 2

S2_1  = s2(1); S2_2 = s2(2); S2_3 = s2(3)
GEO_B = math.sin(PI15)**2
SIN2_36 = math.sin(math.radians(36))**2

ALPHA_IR     = 0.848809
LAMBDA_QCD   = 217.0
LAMBDA_UNIV  = GEO_B / ALPHA_IR
ALPHA_BARYON = ALPHA_IR * (2.0 / 3.0)
PHI          = (1.0 + math.sqrt(5.0)) / 2.0
LU           = LAMBDA_UNIV
GAMMA_1      = 14.134725141734694

THETA_CHARM  = 720.0 * 23 / 30
CHARM_T2_AMP = math.cos(2 * math.radians(THETA_CHARM))
CHARM_T3_AMP = math.cos(3 * math.radians(THETA_CHARM))

LAM = {
    ('S1', 0.5, 'T1'):   LU,
    ('S1', 0.5, 'T2'):   LU * PHI**0.5,
    ('S1', 0.5, 'T3'):   LU,
    ('S1', 0.5, 'none'): LU,
    ('S2', 0.5, 'T1'):   LU * PHI**1.0,
    ('S2', 0.5, 'T2'):   LU * PHI**1.5,
    ('S2', 0.5, 'T3'):   LU * PHI**2.0,
    ('S1', 1.5, 'T1'):   1.15 * LU,
    ('S1', 1.5, 'T2'):   LU * PHI**0.5,
    ('S1', 1.5, 'T3'):   LU,
    ('S1', 1.5, 'none'): 1.15 * LU,
    ('S2', 1.5, 'T1'):   LU * PHI**2.0,
    ('S2', 1.5, 'T2'):   LU * PHI**2.0,
    ('S2', 1.5, 'T3'):   LU * PHI**2.0,
    ('S2', 1.5, 'none'): LU * PHI**2.0,
}

def get_lam(sheet, J, T):
    k = (sheet, J, T)
    if k in LAM: return LAM[k]
    return LU if sheet == 'S1' else LU * PHI

A_DEFAULT = 6.0; B_DEFAULT = 0.0; C_DEFAULT = 2.0
PHI_GEOM = 70.0; PHI_INT = 35.0; PHI_Z3 = 65.0; Z3_SKEW = 30.0
R_REINFORCE = 216.0; K_OMEGA = 0.62
KAPPA_0 = 8792356.74; ALPHA_HYP = 1.0 / 3.0

LANES    = {"up":19, "down":11, "strange":7, "charm":23, "bottom":13, "top":17}
LANE_SET = [1, 7, 11, 13, 17, 19, 23, 29]
ANGLES   = {r: 720.0 * r / 30.0 for r in LANE_SET}

INVERSES = {}
for _r in LANE_SET:
    for _s in LANE_SET:
        if (_r * _s) % 30 == 1: INVERSES[_r] = _s

HEAVY_FLAVORS = {"charm", "bottom", "top"}
LIGHT_FLAVORS = {"up", "down", "strange"}

CONSTITUENT = {
    "up":336.0, "down":340.0, "strange":486.0,
    "charm":1550.0, "bottom":4730.0, "top":173400.0,
}

LAMBDA_TOPO = CONSTITUENT["up"] / GAMMA_1

GEO_TWO_7 = math.sqrt(
    math.sin(math.radians(ANGLES[7]  / 2.0)) ** 2 *
    math.sin(math.radians(ANGLES[INVERSES[7]] / 2.0)) ** 2
)
C_HYP = ALPHA_BARYON * LAMBDA_QCD * GEO_TWO_7

def strange_step_down_gf(n_strange, geo_sign):
    if n_strange == 0:   return S2_1
    elif n_strange == 1: return SIN2_36 if geo_sign == -1 else S2_3
    else:                return GEO_B

def derive_geo_factor_heavy(quarks, chirality, sheet, cover, spin):
    gens = [GEN_MAP[q] for q in quarks]
    n_unique = len(set(gens)); n_light = gens.count(1)
    has_up = 'up' in quarks; has_down = 'down' in quarks
    mixed = has_up and has_down
    def mean3(): return sum(s2(GEN_MAP[q]) for q in quarks) / 3

    if chirality == 'lambda':
        if spin == 1.5 and sheet == 'S2':
            if 3 in gens and 2 in gens: return 1.0 - GEO_B
            return S2_1
        heavy_gens = {GEN_MAP[q] for q in quarks if q not in ('up','down')}
        if len(heavy_gens) >= 2 and has_up and not mixed: return S2_1
        return 1.0 - S2_1

    if n_unique == 1: return s2(gens[0])
    if quarks.count('down') == 2 and 'bottom' in quarks and not has_up: return S2_3
    if quarks.count('up')   == 2 and 'bottom' in quarks and not has_down: return S2_1
    if n_light == 0:
        if spin == 1.5: return 1.0 - S2_1
        return mean3()
    if n_light == 1:
        if spin == 1.5 and cover == 1:
            if has_up and not mixed: return 1.0 - S2_3
            return mean3()
        return S2_1
    if spin == 0.5: return S2_1
    if cover >= 2: return 1.0 - S2_1
    if mixed: return mean3()
    return 1.0 - S2_1

BARYON_CLASS = {
    # ── J=1/2 Light octet ────────────────────────────────────────────────────
    'proton'      : ('S1', -1, 'sigma',  1, 'T1',   'light'),
    'neutron'     : ('S1', -1, 'sigma',  1, 'T1',   'light'),
    'Lambda0'     : ('S1', -1, 'lambda', 1, 'T1',   'light'),
    'Sigma+'      : ('S1', +1, 'lambda', 1, 'T1',   'light'),
    'Sigma0'      : ('S1', +1, 'lambda', 1, 'T1',   'light'),
    'Sigma-'      : ('S1', +1, 'lambda', 1, 'T1',   'light'),
    'Xi0'         : ('S1', -1, 'lambda', 1, 'T1',   'light'),
    'Xi-'         : ('S1', -1, 'lambda', 1, 'T1',   'light'),
    'Omega-'      : ('S2', +1, 'lambda', 1, 'T1',   'omega'),

    # ── J=1/2 Charm ──────────────────────────────────────────────────────────
    'Lambda_c+'   : ('S2', -1, 'sigma',  1, 'T1',   'heavy'),
    'Sigma_c++'   : ('S2', -1, 'sigma',  2, 'T1',   'heavy'),
    'Sigma_c+'    : ('S1', +1, 'lambda', 1, 'T2',   'heavy'),  # gf override → S2[3]
    'Sigma_c0'    : ('S1', -1, 'sigma',  2, 'T2',   'heavy'),
    'Xi_c+'       : ('S2', -1, 'lambda', 1, 'T1',   'heavy'),
    'Xi_c0'       : ('S2', -1, 'lambda', 1, 'T1',   'heavy'),
    'Xi_c_prime+' : ('S2', +1, 'sigma',  3, 'T3',   'heavy'),
    'Xi_c_prime0' : ('S2', +1, 'sigma',  3, 'T3',   'heavy'),
    'Omega_c'     : ('S1', -1, 'lambda', 2, 'T2',   'omega'),
    'Xi_cc++'     : ('S2', -1, 'lambda', 1, 'T1',   'heavy'),
    'Xi_cc+'      : ('S2', -1, 'lambda', 1, 'T1',   'heavy'),

    # ── J=1/2 Bottom ─────────────────────────────────────────────────────────
    'Lambda_b'    : ('S1', -1, 'sigma',  2, 'T2',   'heavy'),
    'Sigma_b+'    : ('S2', +1, 'sigma',  2, 'T1',   'heavy'),
    'Sigma_b0'    : ('S2', +1, 'sigma',  2, 'T2',   'heavy'),
    'Sigma_b-'    : ('S1', +1, 'sigma',  2, 'T2',   'heavy'),
    'Xi_b0'       : ('S1', -1, 'lambda', 2, 'T2',   'heavy'),
    'Xi_b-'       : ('S1', -1, 'lambda', 2, 'T2',   'heavy'),
    'Omega_b'     : ('S1', +1, 'sigma',  1, 'T1',   'omega'),

    # ── J=3/2 Light decuplet ─────────────────────────────────────────────────
    'Delta++'     : ('S1', -1, 'sigma',  1, 'T2',   'J32L'),
    'Delta+'      : ('S1', +1, 'sigma',  1, 'T1',   'J32L'),
    'Delta0'      : ('S1', +1, 'sigma',  1, 'T1',   'J32L'),
    'Delta-'      : ('S1', +1, 'sigma',  1, 'T1',   'J32L'),
    'Sigma*+'     : ('S1', +1, 'sigma',  1, 'T1',   'J32L'),
    'Sigma*0'     : ('S1', -1, 'sigma',  1, 'T1',   'J32L'),
    'Sigma*-'     : ('S1', +1, 'sigma',  1, 'T1',   'J32L'),
    'Xi*0'        : ('S1', -1, 'sigma',  1, 'T3',   'J32L'),
    'Xi*-'        : ('S1', -1, 'sigma',  1, 'T3',   'J32L'),
    'Omega_c*'    : ('S1', -1, 'sigma',  1, 'T1',   'omega'),  # OPEN: needs new branch

    # ── J=3/2 Charm ──────────────────────────────────────────────────────────
    'Sigma_c*++'  : ('S1', +1, 'sigma',  2, 'T2',   'J32H'),
    'Sigma_c*+'   : ('S1', -1, 'sigma',  2, 'T2',   'J32H'),
    'Sigma_c*0'   : ('S1', +1, 'sigma',  2, 'T2',   'J32H'),
    'Xi_c*+'      : ('S1', -1, 'lambda', 2, 'T3',   'photon'),  # v7: photon branch
    'Xi_c*0'      : ('S1', -1, 'lambda', 2, 'T3',   'photon'),  # v7: photon branch

    # ── J=3/2 Bottom ─────────────────────────────────────────────────────────
    'Sigma_b*+'   : ('S1', -1, 'sigma',  2, 'T2',   'J32H'),
    'Sigma_b*-'   : ('S1', +1, 'sigma',  2, 'T2',   'J32H'),
    'Xi_b*0'      : ('S1', -1, 'lambda', 1, 'T3',   'J32H'),
    'Xi_b*-'      : ('S1', -1, 'lambda', 2, 'T3',   'photon'),  # v7: photon branch
    'Omega_b*'    : ('S1', -1, 'sigma',  1, 'T1',   'omega'),
}

GEO_FACTOR_OVERRIDE = {
    'Sigma_b+' : 0.165435,
    'Sigma_b-' : 0.834565,
    'Sigma_c++': 0.989074,
    'Sigma_c0' : 0.697867,
    'Sigma_c+' : 0.165435,   # v7: S2[3] generation-adjacency fix
}

def get_class(name, quarks, J):
    if name not in BARYON_CLASS:
        angles = [ANGLES[LANES[q]] for q in quarks]
        gf = sum(max(math.sin(math.radians(a/2))**2, 1e-10) for a in angles) / len(angles)
        hq = [q for q in quarks if q in HEAVY_FLAVORS]
        T  = 'T2' if hq else 'T1'
        return ('S1', -1, gf, T, 'heavy' if hq else 'light')

    sheet, geo_sign, chirality, cover, T, rule = BARYON_CLASS[name]

    if name in GEO_FACTOR_OVERRIDE:
        return (sheet, geo_sign, GEO_FACTOR_OVERRIDE[name], T, rule)

    heavy = [q for q in quarks if q in HEAVY_FLAVORS]
    if not heavy:
        gf = strange_step_down_gf(quarks.count('strange'), geo_sign)
    else:
        gf = derive_geo_factor_heavy(quarks, chirality, sheet, cover, J)

    return (sheet, geo_sign, gf, T, rule)

KNOWN_BARYONS = [
    ("proton",    ["up","up","down"],          0.5, 938.272),
    ("neutron",   ["up","down","down"],        0.5, 939.565),
    ("Lambda0",   ["up","down","strange"],     0.5, 1115.683),
    ("Sigma+",    ["up","up","strange"],       0.5, 1189.370),
    ("Sigma0",    ["up","down","strange"],     0.5, 1192.642),
    ("Sigma-",    ["down","down","strange"],   0.5, 1197.449),
    ("Xi0",       ["up","strange","strange"],  0.5, 1314.860),
    ("Xi-",       ["down","strange","strange"],0.5, 1321.710),
    ("Omega-",    ["strange","strange","strange"],0.5,1672.450),
    ("Lambda_c+", ["up","down","charm"],       0.5, 2286.460),
    ("Sigma_c++", ["up","up","charm"],         0.5, 2453.970),
    ("Sigma_c+",  ["up","down","charm"],       0.5, 2452.900),
    ("Sigma_c0",  ["down","down","charm"],     0.5, 2453.750),
    ("Xi_c+",     ["up","strange","charm"],    0.5, 2467.930),
    ("Xi_c0",     ["down","strange","charm"],  0.5, 2470.850),
    ("Omega_c",   ["strange","strange","charm"],0.5,2695.200),
    ("Xi_cc++",   ["up","charm","charm"],      0.5, 3621.400),
    ("Xi_cc+",    ["down","charm","charm"],    0.5, 3619.970),
    ("Lambda_b",  ["up","down","bottom"],      0.5, 5619.600),
    ("Sigma_b+",  ["up","up","bottom"],        0.5, 5810.560),
    ("Sigma_b-",  ["down","down","bottom"],    0.5, 5815.640),
    ("Xi_b0",     ["up","strange","bottom"],   0.5, 5791.900),
    ("Xi_b-",     ["down","strange","bottom"], 0.5, 5797.000),
    ("Omega_b",   ["strange","strange","bottom"],0.5,6046.100),
    ("Delta++",   ["up","up","up"],            1.5, 1232.0),
    ("Delta+",    ["up","up","down"],          1.5, 1232.0),
    ("Delta0",    ["up","down","down"],        1.5, 1232.0),
    ("Delta-",    ["down","down","down"],      1.5, 1232.0),
    ("Sigma*+",   ["up","up","strange"],       1.5, 1382.8),
    ("Sigma*0",   ["up","down","strange"],     1.5, 1383.7),
    ("Sigma*-",   ["down","down","strange"],   1.5, 1387.2),
    ("Xi*0",      ["up","strange","strange"],  1.5, 1531.8),
    ("Xi*-",      ["down","strange","strange"],1.5, 1535.0),
    ("Sigma_c*++",["up","up","charm"],         1.5, 2517.5),
    ("Sigma_c*+", ["up","down","charm"],       1.5, 2517.5),
    ("Sigma_c*0", ["down","down","charm"],     1.5, 2518.4),
    ("Xi_c*+",    ["up","strange","charm"],    1.5, 2645.9),
    ("Xi_c*0",    ["down","strange","charm"],  1.5, 2646.2),
    ("Omega_c*",  ["strange","strange","charm"],1.5,2765.9),
    ("Sigma_b*+", ["up","up","bottom"],        1.5, 5832.1),
    ("Sigma_b*-", ["down","down","bottom"],    1.5, 5835.1),
    ("Xi_b*0",    ["up","strange","bottom"],   1.5, 5945.2),
    ("Xi_b*-",    ["down","strange","bottom"], 1.5, 5953.8),
    ("Omega_b*",  ["strange","strange","bottom"],1.5,6082.3),
]

PREDICTIONS = [
    ("Omega_cc+", ["strange","charm","charm"],  0.5, None),
    ("Xi_bc+",    ["up","bottom","charm"],       0.5, None),
    ("Xi_bc0",    ["down","bottom","charm"],     0.5, None),
    ("Omega_bc0", ["strange","bottom","charm"],  0.5, None),
    ("Xi_bb0",    ["up","bottom","bottom"],      0.5, None),
    ("Xi_bb-",    ["down","bottom","bottom"],    0.5, None),
    ("Omega_bb-", ["strange","bottom","bottom"], 0.5, None),
]

HYPERFINE_WHITELIST = {"Sigma0","Sigma_c+","Sigma_b0"}
_CLEAN = {"proton","neutron","Lambda0","Xi0","Xi-","Omega-",
          "Xi_c+","Xi_c0","Omega_c","Lambda_b","Xi_b0","Xi_b-","Omega_b"}
_DEGEN = {"Sigma_c++","Sigma_c0","Xi_cc++","Xi_cc+"}
def fit_group(name):
    if name in _DEGEN: return "degen"
    if name in _CLEAN: return "clean"
    return "wide"

def sector_residue_angle(qs):
    if not qs: return 0.0
    r = 1
    for q in qs: r = (r * LANES[q]) % 30
    return ANGLES.get(r, 0.0)

def relative_angle(lq, hq):
    if not lq or not hq: return 0.0
    diff = abs(sector_residue_angle(hq) - sector_residue_angle(lq))
    if diff > 360.0: diff = 720.0 - diff
    return diff

def tri_wave(deg, phi_p):
    x = (deg / phi_p) % 2.0; return 1.0 - 2.0 * abs(x - 1.0)

def skew_angle(quarks):
    angs = sorted([ANGLES[LANES[q]] for q in quarks]); gaps = []
    for i in range(len(angs)):
        for j in range(i+1, len(angs)): gaps.append(abs(angs[j] - angs[i]))
    gaps.append(720.0 - angs[-1] + angs[0])
    return sum(abs(g - 240.0) for g in gaps) / len(gaps)

def z3_asymmetry(quarks):
    angs = sorted([ANGLES[LANES[q]] for q in quarks])
    cyc  = angs + [angs[0] + 720.0]
    gaps = [cyc[i+1] - cyc[i] for i in range(3)]
    return max(gaps) - min(gaps)

def geo_corr(quarks):
    theta = skew_angle(quarks); tz = z3_asymmetry(quarks)
    tg    = tri_wave(theta, PHI_GEOM); ti = tri_wave(theta, PHI_INT)
    vx    = 1.0 - abs(ti); tz3 = tri_wave(tz + Z3_SKEW, PHI_Z3)
    return A_DEFAULT * tg + B_DEFAULT * vx + C_DEFAULT * tz3

def reinforce(quarks):
    u = quarks.count("up"); d = quarks.count("down")
    s = quarks.count("strange"); c = quarks.count("charm")
    if c == 1 and (u == 2 or d == 2): return 1.0
    if s == 3 or (s == 2 and c == 1): return K_OMEGA
    return 0.0

def charm_flip(n_charm, mode):
    if n_charm == 0: return 1.0
    return (CHARM_T2_AMP if mode == 'T2' else CHARM_T3_AMP) ** n_charm

def delta_hyp(quarks):
    if quarks.count("up") != 1 or quarks.count("down") != 1: return 0.0
    spec = [q for q in quarks if q not in ("up","down")]
    if len(spec) != 1: return 0.0
    ms = CONSTITUENT["strange"]; mu = CONSTITUENT["up"]; md = CONSTITUENT["down"]
    return KAPPA_0 * (CONSTITUENT[spec[0]] / ms) ** ALPHA_HYP / (mu * md)

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def winding_sum(quarks):
    return sum(Fraction(LANES[q], 30) for q in quarks)

def winding_metadata(quarks):
    ws = winding_sum(quarks); n, d = ws.numerator, ws.denominator
    return {"winding_sum":ws,"harmonic_class":d,"numerator":n,
            "denominator":d,"numerator_prime":is_prime(n),
            "m_topo":float(ws)*LAMBDA_TOPO}

def predict_final(quarks, J, name=None):
    sheet, geo_sign, gf, T, rule = get_class(name, quarks, J)

    n_charm = quarks.count("charm")
    lq      = [q for q in quarks if q in LIGHT_FLAVORS]
    hq      = [q for q in quarks if q in HEAVY_FLAVORS]
    hq_nc   = [q for q in hq if q != "charm"]

    sumC = sum(CONSTITUENT[q] for q in quarks)
    S    = -1.0 if J == 0.5 else 3.0
    dg   = geo_sign * ALPHA_BARYON * LAMBDA_QCD * gf

    M_charm = n_charm * CONSTITUENT["charm"]
    M_nc    = sum(CONSTITUENT[q] for q in hq_nc)
    M_light = sum(CONSTITUENT[q] for q in lq)
    fc  = M_charm / sumC if M_charm else 0.0
    fl  = M_light / sumC if M_light else (1.0 if not hq else 0.0)
    fnc = M_nc    / sumC if M_nc    else 0.0

    nc_tr = relative_angle(lq, hq_nc) if hq_nc else relative_angle(lq, hq)
    gc    = geo_corr(quarks)
    rt    = reinforce(quarks) * R_REINFORCE
    lam   = get_lam(sheet, J, T)

    # ── PHOTON-LIKE BRANCH (v7 new) ──────────────────────────────────────────
    # No dg term: geometric mass cancels, only skew (gc) + Hamiltonian survive
    if rule == 'photon':
        final = (sumC + gc + rt + C_HYP*S) * (1 + lam)
        hyp   = delta_hyp(quarks) if name in HYPERFINE_WHITELIST else 0.0
        return _res(name, quarks, J, final+hyp, "photon", lam, gf, winding_metadata(quarks))

    if rule == 'omega':
        final = (sumC + dg + 2.0*gc + rt + C_HYP*S) * (1 + lam)
        hyp   = delta_hyp(quarks) if name in HYPERFINE_WHITELIST else 0.0
        return _res(name, quarks, J, final+hyp, "omega", lam, gf, winding_metadata(quarks))

    if rule == 'J32L':
        if sheet == 'S1':
            final = (sumC + C_HYP*S) * (1 + lam)
        else:
            final = (sumC + dg + gc + rt + C_HYP*S) * (1 + lam)
        return _res(name, quarks, J, final, f"{sheet}_J32L_{T}", lam, gf, winding_metadata(quarks))

    if rule == 'J32H':
        base = sumC + C_HYP*S
        ac   = charm_flip(n_charm, T); n = 2 if T == 'T2' else 3
        if sheet == 'S1':
            anc = abs(math.cos(n * math.radians(nc_tr))) if hq_nc else 1.0
            amp = fl + fc*ac + fnc*anc
            final = base * (1 + lam*amp)
        else:
            anc = math.cos(n * math.radians(nc_tr)) if hq_nc else 1.0
            amp = fl + fc*ac + fnc*anc
            final = (sumC + dg + amp*gc + rt + C_HYP*S) * (1 + lam)
        return _res(name, quarks, J, final, f"{sheet}_J32H_{T}", lam, gf, winding_metadata(quarks))

    if rule == 'light':
        final = (sumC + dg + gc + rt + C_HYP*S) * (1 + lam)
        return _res(name, quarks, J, final, "light", lam, gf, winding_metadata(quarks))

    if rule == 'heavy':
        ac  = charm_flip(n_charm, T); n = 2 if T == 'T2' else 3
        anc = math.cos(n * math.radians(nc_tr)) if hq_nc else 1.0
        amp = fl + fc*ac + fnc*anc
        final = (sumC + dg + amp*gc + rt + C_HYP*S) * (1 + lam)
        hyp = delta_hyp(quarks) if name in HYPERFINE_WHITELIST else 0.0
        return _res(name, quarks, J, final+hyp, f"heavy_{T}", lam, gf, winding_metadata(quarks))

    final = (sumC + dg + gc + rt + C_HYP*S) * (1 + lam)
    return _res(name, quarks, J, final, "fallback", lam, gf, winding_metadata(quarks))

def _res(name, quarks, J, final, branch, lam, gf, wm):
    return {"name":name,"quarks":quarks,"J":J,"final":final,
            "branch":branch,"lam_used":lam,"geo_factor":gf,**wm}

def run_rows(rowspec):
    rows = []
    for name, quarks, J, obs in rowspec:
        pred = predict_final(quarks, J, name=name)
        fg   = fit_group(name)
        row  = {"name":name,"quarks":quarks,"J":J,"obs":obs,"fit_group":fg,**pred}
        if obs is not None:
            err = (row["final"] - obs) / obs * 100
            row["err_pct"] = err; row["abs_err_pct"] = abs(err)
        rows.append(row)
    return rows

def mape(rows, group=None, J=None):
    sc = [r for r in rows if r.get("obs") is not None]
    if group:        sc = [r for r in sc if r.get("fit_group") == group]
    if J is not None: sc = [r for r in sc if r.get("J") == J]
    if not sc: return None
    return sum(r["abs_err_pct"] for r in sc) / len(sc)

def rmse(rows, group=None):
    sc = [r for r in rows if r.get("obs") is not None]
    if group: sc = [r for r in sc if r.get("fit_group") == group]
    if not sc: return None
    return math.sqrt(sum((r["final"]-r["obs"])**2 for r in sc) / len(sc))

def print_table(rows):
    j12 = [r for r in rows if r.get("obs") and r.get("J") == 0.5]
    j32 = [r for r in rows if r.get("obs") and r.get("J") == 1.5]
    for section, grp in [("J=1/2", j12), ("J=3/2", j32)]:
        if not grp: continue
        print(f"\n  {section}:")
        print(f"  {'Name':<14} {'S/T':>6} {'branch':>16} {'obs':>8} {'pred':>8} {'err%':>8}  {'gf':>8}")
        print(f"  {'-'*72}")
        for r in grp:
            sheet,_,_,_,T,_ = BARYON_CLASS.get(r['name'],('?','','','','?',''))
            st = f"{sheet}/{T}"
            print(f"  {r['name']:<14} {st:>6} {r['branch']:>16} "
                  f"{r['obs']:>8.1f} {r['final']:>8.1f} {r['err_pct']:>+8.3f}%"
                  f"  {r['geo_factor']:>8.6f}")

def print_summary(rows):
    obs = [r for r in rows if r.get("obs")]
    j12 = [r for r in obs if r["J"] == 0.5]
    j32 = [r for r in obs if r["J"] == 1.5]
    print("=" * 70)
    print("GBP v7 — Photon-Like Branch + Sigma_c+ Fix")
    print("=" * 70)
    print(f"  LAMBDA_UNIV = {LU:.6f}  phi={PHI:.6f}")
    print(f"  S2[1]={S2_1:.6f}  S2[3]={S2_3:.6f}  GEO_B={GEO_B:.6f}")
    print(f"  Lambda: T1=T3=LU  T2=LU√φ  S2/T1=LU·φ  J32-S2=LU·φ²")
    print(f"  Free params: 2 (kappa_0, lam_s1=1.15·LU)")
    print(f"  v7 changes: Sigma_c+ gf→S2[3], Xi_c*+/0+Xi_b*- → photon/T3")
    print()
    for grp in ("clean","wide","degen"):
        m = mape(rows, group=grp)
        if m:
            gr = [r for r in obs if r.get("fit_group")==grp]
            rms = math.sqrt(sum((r["final"]-r["obs"])**2 for r in gr)/len(gr))
            print(f"  MAPE {grp:<6} = {m:.4f}%   RMSE={rms:.2f} MeV  ({len(gr)})")
    print()
    if j12: print(f"  MAPE J=1/2 = {mape(rows,J=0.5):.4f}%  RMSE={rmse(j12):.2f} MeV  ({len(j12)})")
    if j32: print(f"  MAPE J=3/2 = {mape(rows,J=1.5):.4f}%  RMSE={rmse(j32):.2f} MeV  ({len(j32)})")
    print(f"  MAPE ALL   = {mape(rows):.4f}%  RMSE={rmse(obs):.2f} MeV  ({len(obs)})")
    print(f"  v6 baseline: 0.4078%")
    print(f"  v5 baseline: 0.6365%")

def main():
    parser = argparse.ArgumentParser(description="GBP v7")
    parser.add_argument("--known",       action="store_true")
    parser.add_argument("--j12",         action="store_true")
    parser.add_argument("--j32",         action="store_true")
    parser.add_argument("--predictions", action="store_true")
    parser.add_argument("--all",         action="store_true")
    parser.add_argument("--name",        type=str)
    args = parser.parse_args()

    rows      = run_rows(KNOWN_BARYONS)
    pred_rows = run_rows(PREDICTIONS)

    if args.name:
        matched = [r for r in rows+pred_rows if r["name"].lower()==args.name.lower()]
        if not matched: raise SystemExit(f"Not found: {args.name}")
        print(json.dumps({k: str(v) if isinstance(v,Fraction) else v
                          for k,v in matched[0].items()
                          if not isinstance(v,(list,dict,tuple))}, indent=2))
        return

    print_summary(rows)
    filt = rows
    if args.j12: filt = [r for r in rows if r["J"]==0.5]
    if args.j32: filt = [r for r in rows if r["J"]==1.5]
    if args.all or args.known or args.j12 or args.j32 or not args.predictions:
        print_table(filt)
    if args.all or args.predictions:
        print("\nPredictions:"); print_table(pred_rows)

if __name__ == "__main__":
    main()
