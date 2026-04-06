#!/usr/bin/env python3
"""
gbp_v7_ablation.py — GBP v7 Ablation Study
============================================
Removes one ingredient at a time and reports MAPE/RMSE change.
This is the audit trail that answers: which parts are load-bearing?

Ablation tests:
  0. Full model (baseline)
  1. Remove gc (geo_corr — triangle wave skew correction)
  2. Remove rt (reinforce term)
  3. Remove lam (set all lambda=0)
  4. Remove hyperfine (kappa_0=0)
  5. Remove photon branch (force to J32H)
  6. Remove all geo_factor overrides
  7. Force all baryons to S1/T1 (single topology)
  8. Replace geo_factors with constant=S2[1] for all
  9. Remove dg term (geo_factor contribution)
 10. Constituent sum only (sumC + C_HYP*S — no corrections)

Run: python3 gbp_v7_ablation.py
"""

import math
from fractions import Fraction
from copy import deepcopy

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
    ('S2', 0.5, 'T1'):   LU * PHI**1.0,
    ('S2', 0.5, 'T2'):   LU * PHI**1.5,
    ('S2', 0.5, 'T3'):   LU * PHI**2.0,
    ('S1', 1.5, 'T1'):   1.15 * LU,
    ('S1', 1.5, 'T2'):   LU * PHI**0.5,
    ('S1', 1.5, 'T3'):   LU,
    ('S2', 1.5, 'T1'):   LU * PHI**2.0,
    ('S2', 1.5, 'T2'):   LU * PHI**2.0,
    ('S2', 1.5, 'T3'):   LU * PHI**2.0,
}
def get_lam(sheet, J, T): return LAM.get((sheet, J, T), LU if sheet=='S1' else LU*PHI)

A_DEFAULT=6.0; B_DEFAULT=0.0; C_DEFAULT=2.0
PHI_GEOM=70.0; PHI_INT=35.0; PHI_Z3=65.0; Z3_SKEW=30.0
R_REINFORCE=216.0; K_OMEGA=0.62
KAPPA_0=8792356.74; ALPHA_HYP=1.0/3.0

LANES    = {"up":19,"down":11,"strange":7,"charm":23,"bottom":13,"top":17}
LANE_SET = [1,7,11,13,17,19,23,29]
ANGLES   = {r: 720.0*r/30.0 for r in LANE_SET}
INVERSES = {}
for _r in LANE_SET:
    for _s in LANE_SET:
        if (_r*_s)%30==1: INVERSES[_r]=_s

HEAVY_FLAVORS = {"charm","bottom","top"}
LIGHT_FLAVORS = {"up","down","strange"}
CONSTITUENT = {
    "up":336.0,"down":340.0,"strange":486.0,
    "charm":1550.0,"bottom":4730.0,"top":173400.0,
}
GEO_TWO_7 = math.sqrt(
    math.sin(math.radians(ANGLES[7]/2.0))**2 *
    math.sin(math.radians(ANGLES[INVERSES[7]]/2.0))**2
)
C_HYP = ALPHA_BARYON * LAMBDA_QCD * GEO_TWO_7

def strange_step_down_gf(n_strange, geo_sign):
    if n_strange==0:   return S2_1
    elif n_strange==1: return SIN2_36 if geo_sign==-1 else S2_3
    else:              return GEO_B

def derive_geo_factor_heavy(quarks, chirality, sheet, cover, spin):
    gens=[GEN_MAP[q] for q in quarks]
    n_unique=len(set(gens)); n_light=gens.count(1)
    has_up='up' in quarks; has_down='down' in quarks
    mixed=has_up and has_down
    def mean3(): return sum(s2(GEN_MAP[q]) for q in quarks)/3
    if chirality=='lambda':
        if spin==1.5 and sheet=='S2':
            if 3 in gens and 2 in gens: return 1.0-GEO_B
            return S2_1
        heavy_gens={GEN_MAP[q] for q in quarks if q not in ('up','down')}
        if len(heavy_gens)>=2 and has_up and not mixed: return S2_1
        return 1.0-S2_1
    if n_unique==1: return s2(gens[0])
    if quarks.count('down')==2 and 'bottom' in quarks and not has_up: return S2_3
    if quarks.count('up')==2   and 'bottom' in quarks and not has_down: return S2_1
    if n_light==0:
        if spin==1.5: return 1.0-S2_1
        return mean3()
    if n_light==1:
        if spin==1.5 and cover==1:
            if has_up and not mixed: return 1.0-S2_3
            return mean3()
        return S2_1
    if spin==0.5: return S2_1
    if cover>=2: return 1.0-S2_1
    if mixed: return mean3()
    return 1.0-S2_1

BARYON_CLASS = {
    'proton'      :('S1',-1,'sigma', 1,'T1','light'),
    'neutron'     :('S1',-1,'sigma', 1,'T1','light'),
    'Lambda0'     :('S1',-1,'lambda',1,'T1','light'),
    'Sigma+'      :('S1',+1,'lambda',1,'T1','light'),
    'Sigma0'      :('S1',+1,'lambda',1,'T1','light'),
    'Sigma-'      :('S1',+1,'lambda',1,'T1','light'),
    'Xi0'         :('S1',-1,'lambda',1,'T1','light'),
    'Xi-'         :('S1',-1,'lambda',1,'T1','light'),
    'Omega-'      :('S2',+1,'lambda',1,'T1','omega'),
    'Lambda_c+'   :('S2',-1,'sigma', 1,'T1','heavy'),
    'Sigma_c++'   :('S2',-1,'sigma', 2,'T1','heavy'),
    'Sigma_c+'    :('S1',+1,'lambda',1,'T2','heavy'),
    'Sigma_c0'    :('S1',-1,'sigma', 2,'T2','heavy'),
    'Xi_c+'       :('S2',-1,'lambda',1,'T1','heavy'),
    'Xi_c0'       :('S2',-1,'lambda',1,'T1','heavy'),
    'Xi_c_prime+' :('S2',+1,'sigma', 3,'T3','heavy'),
    'Xi_c_prime0' :('S2',+1,'sigma', 3,'T3','heavy'),
    'Omega_c'     :('S1',-1,'lambda',2,'T2','omega'),
    'Xi_cc++'     :('S2',-1,'lambda',1,'T1','heavy'),
    'Xi_cc+'      :('S2',-1,'lambda',1,'T1','heavy'),
    'Lambda_b'    :('S1',-1,'sigma', 2,'T2','heavy'),
    'Sigma_b+'    :('S2',+1,'sigma', 2,'T1','heavy'),
    'Sigma_b0'    :('S2',+1,'sigma', 2,'T2','heavy'),
    'Sigma_b-'    :('S1',+1,'sigma', 2,'T2','heavy'),
    'Xi_b0'       :('S1',-1,'lambda',2,'T2','heavy'),
    'Xi_b-'       :('S1',-1,'lambda',2,'T2','heavy'),
    'Omega_b'     :('S1',+1,'sigma', 1,'T1','omega'),
    'Delta++'     :('S1',-1,'sigma', 1,'T2','J32L'),
    'Delta+'      :('S1',+1,'sigma', 1,'T1','J32L'),
    'Delta0'      :('S1',+1,'sigma', 1,'T1','J32L'),
    'Delta-'      :('S1',+1,'sigma', 1,'T1','J32L'),
    'Sigma*+'     :('S1',+1,'sigma', 1,'T1','J32L'),
    'Sigma*0'     :('S1',-1,'sigma', 1,'T1','J32L'),
    'Sigma*-'     :('S1',+1,'sigma', 1,'T1','J32L'),
    'Xi*0'        :('S1',-1,'sigma', 1,'T3','J32L'),
    'Xi*-'        :('S1',-1,'sigma', 1,'T3','J32L'),
    'Omega_c*'    :('S1',-1,'sigma', 1,'T1','omega'),
    'Sigma_c*++'  :('S1',+1,'sigma', 2,'T2','J32H'),
    'Sigma_c*+'   :('S1',-1,'sigma', 2,'T2','J32H'),
    'Sigma_c*0'   :('S1',+1,'sigma', 2,'T2','J32H'),
    'Xi_c*+'      :('S1',-1,'lambda',2,'T3','photon'),
    'Xi_c*0'      :('S1',-1,'lambda',2,'T3','photon'),
    'Sigma_b*+'   :('S1',-1,'sigma', 2,'T2','J32H'),
    'Sigma_b*-'   :('S1',+1,'sigma', 2,'T2','J32H'),
    'Xi_b*0'      :('S1',-1,'lambda',1,'T3','J32H'),
    'Xi_b*-'      :('S1',-1,'lambda',2,'T3','photon'),
    'Omega_b*'    :('S1',-1,'sigma', 1,'T1','omega'),
}

GEO_FACTOR_OVERRIDE = {
    'Sigma_b+' :0.165435,
    'Sigma_b-' :0.834565,
    'Sigma_c++':0.989074,
    'Sigma_c0' :0.697867,
    'Sigma_c+' :0.165435,
}

HYPERFINE_WHITELIST = {"Sigma0","Sigma_c+","Sigma_b0"}

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

# ── GEOMETRY ─────────────────────────────────────────────────────────────────
def sector_residue_angle(qs):
    if not qs: return 0.0
    r=1
    for q in qs: r=(r*LANES[q])%30
    return ANGLES.get(r,0.0)

def relative_angle(lq,hq):
    if not lq or not hq: return 0.0
    diff=abs(sector_residue_angle(hq)-sector_residue_angle(lq))
    if diff>360.0: diff=720.0-diff
    return diff

def tri_wave(deg,phi_p):
    x=(deg/phi_p)%2.0; return 1.0-2.0*abs(x-1.0)

def skew_angle(quarks):
    angs=sorted([ANGLES[LANES[q]] for q in quarks]); gaps=[]
    for i in range(len(angs)):
        for j in range(i+1,len(angs)): gaps.append(abs(angs[j]-angs[i]))
    gaps.append(720.0-angs[-1]+angs[0])
    return sum(abs(g-240.0) for g in gaps)/len(gaps)

def z3_asymmetry(quarks):
    angs=sorted([ANGLES[LANES[q]] for q in quarks])
    cyc=angs+[angs[0]+720.0]
    gaps=[cyc[i+1]-cyc[i] for i in range(3)]
    return max(gaps)-min(gaps)

def geo_corr(quarks):
    theta=skew_angle(quarks); tz=z3_asymmetry(quarks)
    tg=tri_wave(theta,PHI_GEOM); ti=tri_wave(theta,PHI_INT)
    vx=1.0-abs(ti); tz3=tri_wave(tz+Z3_SKEW,PHI_Z3)
    return A_DEFAULT*tg+B_DEFAULT*vx+C_DEFAULT*tz3

def reinforce(quarks):
    u=quarks.count("up"); d=quarks.count("down")
    s=quarks.count("strange"); c=quarks.count("charm")
    if c==1 and (u==2 or d==2): return 1.0
    if s==3 or (s==2 and c==1): return K_OMEGA
    return 0.0

def charm_flip(n_charm,mode):
    if n_charm==0: return 1.0
    return (CHARM_T2_AMP if mode=='T2' else CHARM_T3_AMP)**n_charm

def delta_hyp(quarks):
    if quarks.count("up")!=1 or quarks.count("down")!=1: return 0.0
    spec=[q for q in quarks if q not in ("up","down")]
    if len(spec)!=1: return 0.0
    ms=CONSTITUENT["strange"]; mu=CONSTITUENT["up"]; md=CONSTITUENT["down"]
    return KAPPA_0*(CONSTITUENT[spec[0]]/ms)**ALPHA_HYP/(mu*md)

# ── CORE PREDICTOR WITH ABLATION FLAGS ───────────────────────────────────────
def predict(quarks, J, name, flags):
    """
    flags dict controls ablations:
      no_gc       : set gc=0
      no_rt       : set rt=0
      no_lam      : set lam=0
      no_hyp      : set kappa_0=0
      no_photon   : treat photon branch as J32H
      no_overrides: skip GEO_FACTOR_OVERRIDE
      force_S1T1  : force all to S1/T1
      const_gf    : replace all geo_factors with S2[1]
      no_dg       : set dg=0
      sumC_only   : return (sumC + C_HYP*S) only
    """
    # Get classification
    if flags.get('force_S1T1'):
        sheet,geo_sign,chirality,cover,T,rule = 'S1',-1,'sigma',1,'T1','light'
        heavy=[q for q in quarks if q in HEAVY_FLAVORS]
        if heavy: rule='heavy'
    elif name in BARYON_CLASS:
        sheet,geo_sign,chirality,cover,T,rule = BARYON_CLASS[name]
    else:
        sheet,geo_sign,chirality,cover,T,rule = 'S1',-1,'sigma',1,'T1','light'

    # Get geo_factor
    if flags.get('const_gf'):
        gf = S2_1
    elif not flags.get('no_overrides') and name in GEO_FACTOR_OVERRIDE:
        gf = GEO_FACTOR_OVERRIDE[name]
    else:
        heavy=[q for q in quarks if q in HEAVY_FLAVORS]
        if not heavy:
            gf=strange_step_down_gf(quarks.count('strange'),geo_sign)
        else:
            gf=derive_geo_factor_heavy(quarks,chirality,sheet,cover,J)

    n_charm=quarks.count("charm")
    lq=[q for q in quarks if q in LIGHT_FLAVORS]
    hq=[q for q in quarks if q in HEAVY_FLAVORS]
    hq_nc=[q for q in hq if q!="charm"]

    sumC=sum(CONSTITUENT[q] for q in quarks)
    S=-1.0 if J==0.5 else 3.0

    # sumC only ablation
    if flags.get('sumC_only'):
        return (sumC+C_HYP*S)

    dg = 0.0 if flags.get('no_dg') else geo_sign*ALPHA_BARYON*LAMBDA_QCD*gf
    gc = 0.0 if flags.get('no_gc') else geo_corr(quarks)
    rt = 0.0 if flags.get('no_rt') else reinforce(quarks)*R_REINFORCE
    lam= 0.0 if flags.get('no_lam') else get_lam(sheet,J,T)
    hyp= 0.0 if flags.get('no_hyp') else (delta_hyp(quarks) if name in HYPERFINE_WHITELIST else 0.0)

    M_charm=n_charm*CONSTITUENT["charm"]
    M_nc=sum(CONSTITUENT[q] for q in hq_nc)
    M_light=sum(CONSTITUENT[q] for q in lq)
    fc=M_charm/sumC if M_charm else 0.0
    fl=M_light/sumC if M_light else (1.0 if not hq else 0.0)
    fnc=M_nc/sumC if M_nc else 0.0
    nc_tr=relative_angle(lq,hq_nc) if hq_nc else relative_angle(lq,hq)

    # photon branch
    eff_rule = rule
    if rule=='photon' and flags.get('no_photon'):
        eff_rule='J32H'

    if eff_rule=='photon':
        return (sumC+gc+rt+C_HYP*S)*(1+lam)+hyp

    if eff_rule=='omega':
        return (sumC+dg+2.0*gc+rt+C_HYP*S)*(1+lam)+hyp

    if eff_rule=='J32L':
        if sheet=='S1':
            return (sumC+C_HYP*S)*(1+lam)
        return (sumC+dg+gc+rt+C_HYP*S)*(1+lam)

    if eff_rule=='J32H':
        base=sumC+C_HYP*S
        ac=charm_flip(n_charm,T); n=2 if T=='T2' else 3
        if sheet=='S1':
            anc=abs(math.cos(n*math.radians(nc_tr))) if hq_nc else 1.0
            amp=fl+fc*ac+fnc*anc
            return base*(1+lam*amp)
        else:
            anc=math.cos(n*math.radians(nc_tr)) if hq_nc else 1.0
            amp=fl+fc*ac+fnc*anc
            return (sumC+dg+amp*gc+rt+C_HYP*S)*(1+lam)

    if eff_rule=='light':
        return (sumC+dg+gc+rt+C_HYP*S)*(1+lam)

    # heavy
    ac=charm_flip(n_charm,T); n=2 if T=='T2' else 3
    anc=math.cos(n*math.radians(nc_tr)) if hq_nc else 1.0
    amp=fl+fc*ac+fnc*anc
    return (sumC+dg+amp*gc+rt+C_HYP*S)*(1+lam)+hyp

def score(flags):
    errs=[]; j12=[]; j32=[]
    for name,quarks,J,obs in KNOWN_BARYONS:
        pred=predict(quarks,J,name,flags)
        e=abs(pred-obs)/obs*100
        errs.append(e)
        if J==0.5: j12.append(e)
        else:      j32.append(e)
    mape_all=sum(errs)/len(errs)
    rmse=math.sqrt(sum((predict(q[1],q[2],q[0],flags)-q[3])**2
                       for q in KNOWN_BARYONS)/len(KNOWN_BARYONS))
    return mape_all, sum(j12)/len(j12), sum(j32)/len(j32), rmse

# ── RUN ALL ABLATIONS ─────────────────────────────────────────────────────────
ABLATIONS = [
    ("0. Full model (baseline)",          {}),
    ("1. Remove gc (triangle wave skew)", {"no_gc":True}),
    ("2. Remove rt (reinforce term)",     {"no_rt":True}),
    ("3. Remove lam (boundary scaling)",  {"no_lam":True}),
    ("4. Remove hyperfine (kappa_0=0)",   {"no_hyp":True}),
    ("5. Remove photon branch",           {"no_photon":True}),
    ("6. Remove geo_factor overrides",    {"no_overrides":True}),
    ("7. Force all S1/T1 topology",       {"force_S1T1":True}),
    ("8. Constant geo_factor=S2[1]",      {"const_gf":True}),
    ("9. Remove dg term",                 {"no_dg":True}),
    ("10. Constituent sum only",          {"sumC_only":True}),
]

print("="*75)
print("GBP v7 — Ablation Study")
print("="*75)
print(f"  {'Test':<38} {'MAPE ALL':>9} {'J=1/2':>7} {'J=3/2':>7} {'RMSE':>8}  {'Δ MAPE':>8}")
print(f"  {'-'*72}")

baseline_mape = None
for label, flags in ABLATIONS:
    m, m12, m32, rmse = score(flags)
    if baseline_mape is None:
        baseline_mape = m
        delta = "—"
    else:
        delta = f"{m-baseline_mape:+.4f}%"
    marker = "  ◄ baseline" if baseline_mape==m else ""
    print(f"  {label:<38} {m:>8.4f}% {m12:>6.4f}% {m32:>6.4f}% {rmse:>7.2f}  {delta}{marker}")

print()
print("="*75)
print("INTERPRETATION")
print("""
  Large ΔMAPE = ingredient is load-bearing (essential)
  Small ΔMAPE = ingredient is redundant or patchwork

  Key questions:
  - Does removing geo_factor overrides collapse accuracy? (test 6)
    If yes: overrides are load-bearing, need physical derivation
    If no:  overrides are cosmetic, model is robust without them

  - Does removing photon branch hurt J=3/2 only? (test 5)
    If yes: photon branch captures real topology, not overfitting
    If no:  photon branch may be redundant

  - Does removing lam hurt more than removing gc? (tests 1 vs 3)
    Tells you whether boundary scaling or skew correction
    is doing more work

  - How far is constituent sum only from full model? (test 10)
    Quantifies total value added by all corrections combined
""")

# ── PER-BARYON BREAKDOWN FOR MOST IMPACTFUL ABLATIONS ────────────────────────
print("="*75)
print("Per-baryon impact of removing geo_factor overrides (test 6)")
print(f"  {'Name':<14} {'obs':>8} {'full':>8} {'no_ovr':>8} {'Δerr':>8}")
print(f"  {'-'*50}")
for name,quarks,J,obs in KNOWN_BARYONS:
    p_full = predict(quarks,J,name,{})
    p_nov  = predict(quarks,J,name,{"no_overrides":True})
    e_full = (p_full-obs)/obs*100
    e_nov  = (p_nov-obs)/obs*100
    delta  = e_nov-e_full
    if abs(delta)>0.01:
        print(f"  {name:<14} {obs:>8.1f} {p_full:>8.1f} {p_nov:>8.1f} {delta:>+8.3f}%")

print()
print("="*75)
print("Per-baryon impact of removing photon branch (test 5)")
print(f"  {'Name':<14} {'obs':>8} {'full':>8} {'no_phot':>8} {'Δerr':>8}")
print(f"  {'-'*50}")
for name,quarks,J,obs in KNOWN_BARYONS:
    p_full = predict(quarks,J,name,{})
    p_nph  = predict(quarks,J,name,{"no_photon":True})
    e_full = (p_full-obs)/obs*100
    e_nph  = (p_nph-obs)/obs*100
    delta  = e_nph-e_full
    if abs(delta)>0.01:
        print(f"  {name:<14} {obs:>8.1f} {p_full:>8.1f} {p_nph:>8.1f} {delta:>+8.3f}%")
