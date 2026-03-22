"""
baryon_residues.py
==================
Mod-30 Spinor Geometry — Baryon Residue Calculator

Computes the residue class of hadrons under the multiplicative rule:
    R = r1 × r2 × r3  (mod 30)  for baryons
    R = r × r_inv     (mod 30)  for mesons  → always 1

The six quark residue assignments come from the V9 mass model.
The two empty quark slots (residues 1 and 29) appear in:
    - Light cascade baryons (Xi0, Xi-)
    - Doubly charmed Xi baryons (Xi_cc++, Xi_cc0)
This cross-scale symmetry is confirmed by the March 2026 LHCb
discovery of Xi_cc0 (ccd) → residue 29.

J. Richardson | Independent Researcher | March 2026
github.com/historyViper/mod30-spinor
"""

# ─── Quark residue assignments (from V9 mass optimization) ───────────────────

RESIDUES = {
    'up':      19,
    'down':    11,
    'strange':  7,
    'charm':   23,
    'bottom':  13,
    'top':     17,
}

# Multiplicative inverses mod 30
# r × r_inv ≡ 1 (mod 30)
INVERSES = {}
units = [1, 7, 11, 13, 17, 19, 23, 29]
for r in units:
    for s in units:
        if (r * s) % 30 == 1:
            INVERSES[r] = s

# ─── Helper functions ─────────────────────────────────────────────────────────

def mod30(x):
    return x % 30

def baryon_residue(q1, q2, q3):
    """Compute residue of a baryon from three quark names."""
    return mod30(RESIDUES[q1] * RESIDUES[q2] * RESIDUES[q3])

def meson_residue(q):
    """All mesons map to 1 (identity)."""
    return mod30(RESIDUES[q] * INVERSES[RESIDUES[q]])

def residue_label(r):
    """Return the quark name for a residue, or 'empty' if unoccupied."""
    for name, res in RESIDUES.items():
        if res == r:
            return name
    return 'empty slot'

def print_table(title, baryons, col_widths=(18, 25, 10, 20)):
    w = col_widths
    print(f"\n{'─'*sum(w)}")
    print(f"  {title}")
    print(f"{'─'*sum(w)}")
    print(f"  {'Baryon':<{w[0]}} {'Quarks':<{w[1]}} {'Residue':>{w[2]}}  {'= Quark slot':<{w[3]}}")
    print(f"  {'─'*(sum(w)-2)}")
    for name, quarks in baryons.items():
        r = baryon_residue(*quarks)
        label = residue_label(r)
        flag = ' ← C₄ step' if label in ('bottom', 'top') else ''
        flag = ' ← boundary' if r in (1, 29) else flag
        print(f"  {name:<{w[0]}} {str(quarks):<{w[1]}} {r:>{w[2]}}  {label}{flag}")

# ─── Baryon tables ─────────────────────────────────────────────────────────────

OCTET = {
    'proton':       ('up',     'up',     'down'),
    'neutron':      ('up',     'down',   'down'),
    'Lambda':       ('up',     'down',   'strange'),
    'Sigma+':       ('up',     'up',     'strange'),
    'Sigma0':       ('up',     'down',   'strange'),
    'Sigma-':       ('down',   'down',   'strange'),
    'Xi0':          ('up',     'strange','strange'),
    'Xi-':          ('down',   'strange','strange'),
}

DECUPLET = {
    'Delta++':      ('up',     'up',     'up'),
    'Delta+':       ('up',     'up',     'down'),
    'Delta0':       ('up',     'down',   'down'),
    'Delta-':       ('down',   'down',   'down'),
    'Sigma*+':      ('up',     'up',     'strange'),
    'Sigma*0':      ('up',     'down',   'strange'),
    'Sigma*-':      ('down',   'down',   'strange'),
    'Xi*0':         ('up',     'strange','strange'),
    'Xi*-':         ('down',   'strange','strange'),
    'Omega-':       ('strange','strange','strange'),
}

CHARM_BARYONS = {
    'Lambda_c':     ('up',     'down',   'charm'),
    'Sigma_c+':     ('up',     'up',     'charm'),
    'Sigma_c0':     ('up',     'down',   'charm'),
    'Xi_c+':        ('up',     'strange','charm'),
    'Xi_c0':        ('down',   'strange','charm'),
    'Omega_c':      ('strange','strange','charm'),
}

BOTTOM_BARYONS = {
    'Lambda_b':     ('up',     'down',   'bottom'),
    'Sigma_b+':     ('up',     'up',     'bottom'),
    'Sigma_b-':     ('down',   'down',   'bottom'),
    'Xi_b0':        ('up',     'strange','bottom'),
    'Xi_b-':        ('down',   'strange','bottom'),
    'Omega_b-':     ('strange','strange','bottom'),
}

DOUBLY_CHARMED = {
    'Xi_cc++ (ccu)':  ('charm', 'charm', 'up'),
    'Xi_cc0  (ccd)':  ('charm', 'charm', 'down'),    # ← LHCb March 17, 2026
    'Omega_cc (ccs)': ('charm', 'charm', 'strange'),
    'Omega_ccc(ccc)': ('charm', 'charm', 'charm'),
}

OMEGA_LADDER = {
    'Omega- (sss)':   ('strange','strange','strange'),
    'Omega_c (ssc)':  ('strange','strange','charm'),
    'Omega_cc (scc)': ('strange','charm',  'charm'),
    'Omega_ccc(ccc)': ('charm',  'charm',  'charm'),
    'Omega_b (ssb)':  ('strange','strange','bottom'),
    'Omega_cb (scb)': ('strange','charm',  'bottom'),
}

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  MOD-30 SPINOR GEOMETRY — BARYON RESIDUE CALCULATOR")
    print("=" * 70)

    # Quark assignments
    print("\n  Quark residue assignments (from V9 mass model):")
    print(f"  {'Quark':<12} {'Residue':>8}  {'θ_spinor':>10}")
    print(f"  {'─'*35}")
    for q, r in RESIDUES.items():
        theta = 24 * r
        print(f"  {q:<12} {r:>8}  {theta:>9}°")
    print(f"\n  Empty slots: residues 1 and 29")

    # Meson check
    print("\n" + "=" * 70)
    print("  MESONS (all map to identity = 1)")
    print("=" * 70)
    print(f"\n  {'Meson':<15} {'Residue':>8}  {'Check'}")
    print(f"  {'─'*40}")
    for q in RESIDUES:
        r = meson_residue(q)
        print(f"  {q+'-anti'+q:<15} {r:>8}  {'✓' if r==1 else '✗'}")

    # Baryon tables
    print_table("BARYON OCTET (J^P = 1/2+)", OCTET)
    print_table("BARYON DECUPLET (J^P = 3/2+)", DECUPLET)
    print_table("CHARM BARYONS", CHARM_BARYONS)
    print_table("BOTTOM BARYONS", BOTTOM_BARYONS)

    # Doubly charmed — key result
    print(f"\n{'═'*70}")
    print("  DOUBLY & TRIPLY CHARMED BARYONS — KEY RESULT")
    print(f"{'═'*70}")
    print(f"\n  {'Baryon':<22} {'Quarks':<25} {'Residue':>8}  {'= Quark slot'}")
    print(f"  {'─'*68}")
    for name, quarks in DOUBLY_CHARMED.items():
        r = baryon_residue(*quarks)
        label = residue_label(r)
        note = ''
        if 'ccd' in name: note = '  ← LHCb March 17, 2026 ✓ CONFIRMED'
        if 'ccu' in name: note = '  ← LHCb 2017 ✓ CONFIRMED'
        if 'Omega_cc ' in name: note = '  ← PREDICTED'
        if 'Omega_ccc' in name: note = '  ← PREDICTED'
        print(f"  {name:<22} {str(quarks):<25} {r:>8}  {label}{note}")

    print(f"\n  Both observed Xi_cc baryons land on empty slots (residues 1 and 29).")
    print(f"  Same empty slots appear in light cascade baryons Xi0 and Xi-.")
    print(f"  Cross-scale symmetry: no additional parameters required.")

    # Omega ladder
    print(f"\n{'═'*70}")
    print("  THE OMEGA LADDER — C₄ GENERATION CYCLE")
    print(f"{'═'*70}")
    print(f"\n  {'Baryon':<22} {'Quarks':<25} {'Residue':>8}  {'= Quark slot'}")
    print(f"  {'─'*68}")
    for name, quarks in OMEGA_LADDER.items():
        r = baryon_residue(*quarks)
        label = residue_label(r)
        print(f"  {name:<22} {str(quarks):<25} {r:>8}  {label}")
    print(f"\n  Residues alternate 13 (bottom) ↔ 17 (top) as charm replaces strange.")
    print(f"  Wraps to strange (7) when bottom is substituted: C₄ cycle closes.")

    # Summary statistics
    all_baryons = {**OCTET, **DECUPLET, **CHARM_BARYONS,
                   **BOTTOM_BARYONS, **DOUBLY_CHARMED}
    all_residues = set(baryon_residue(*q) for q in all_baryons.values())

    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")
    print(f"\n  Residues appearing in baryon spectrum: {sorted(all_residues)}")
    print(f"  Missing: {sorted(set(units) - all_residues)}")
    print(f"\n  All 8 units of (Z/30Z)× appear in the combined baryon spectrum.")
    print(f"  Residues 1 and 29 (empty quark slots) appear as boundary states")
    print(f"  in both light and heavy baryon sectors.")
    print(f"\n  Mesons: all map to residue 1 (identity). ✓")
    print(f"\n  Code: github.com/historyViper/mod30-spinor")

if __name__ == "__main__":
    main()
