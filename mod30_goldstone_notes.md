# Mod-30 Goldstone Bosons and the Pion Decay Constant
## Notes for Part IV — Meson Sector

J. Richardson | March 2026

---

## Key Results (all zero new parameters)

### 1. Goldstone Identification from Boundary Residues

Mesons whose quark × antiquark residue product lands on the boundary slots
(r = 1 or r = 29) are pseudo-Goldstone bosons. This follows purely from the
mod-30 geometry — the boundary slots are the empty quark lanes (no fundamental
quark occupies residues 1 or 29), so a meson winding to the boundary finds no
geometric coupling to complete against. The vortex cannot anchor.

| Meson | q × q̄ residue | Slot | Type |
|-------|----------------|------|------|
| pi+   | 19 × 11 = 29   | Boundary | Goldstone ✓ |
| pi0   | 19 × 19 = 1    | Boundary | Goldstone ✓ |
| eta   | 7 × 13 = 1     | Boundary | Goldstone ✓ |
| K+    | 19 × 13 = 7    | Strange lane | NOT Goldstone ✓ |
| K0    | 11 × 13 = 23   | Charm lane | NOT Goldstone ✓ |

The Goldstone identification is exact and requires no fitting.

### 2. f_pi from Vortex Stiffness (Ginzburg-Landau analogy)

In superfluid analogy (3He-B, Abrikosov vortex, BEC):
- The order parameter amplitude ~ (coupling)^(1/2)
- The Goldstone decay constant (stiffness) ~ (order parameter)^(1/2)
- Combined: decay constant ~ (coupling)^(1/4)

At the boundary vortex the relevant coupling is:
  alpha_q × geo(boundary) = alpha_q × sin²(π/15)

The vortex stiffness formula:

```
f_pi = sqrt(alpha_q) × Lambda_QCD × geo(boundary)^(1/4)
     = sqrt(0.848809) × 217.0 × sin²(π/15)^(1/4)
     = 0.9213 × 217.0 × 0.4561
     = 91.16 MeV
```

**Observed: 92.4 MeV. Error: -1.34%. Zero new parameters.**

Physical interpretation:
- sqrt(alpha_q): field amplitude of QCD coupling (not probability — amplitude)
- Lambda_QCD: coherence length scale of the QCD vacuum
- geo(boundary)^(1/4): two GL square-root steps — order param then stiffness
- The boundary geo = sin²(π/15) is the fundamental angular step of mod-30

This is a first-principles derivation of f_pi from the mod-30 spinor geometry,
motivated by the superfluid/plasma vortex decay constant analogy. No ChPT
coefficients used.

### 3. Chiral Condensate B0

Once f_pi is derived, B0 = Lambda^3 / f_pi^2 = 1229.6 MeV.

The pion mass then follows from:
  m_pi^2 = (m_u + m_d) × B0_effective

where m_u, m_d are PDG current quark masses (2.3, 4.8 MeV) — not free
parameters of this framework.

The current B0 = 1229.6 MeV gives m_pi ~ 94 MeV vs observed 140 MeV.
Remaining discrepancy (~30%) traces to the constructive interference amplitude
of same-angle double helix windings (pi+ = up × anti-down both at 456°).
This geometric factor is the open problem for Part IV.

### 4. Double Helix Physical Interpretation

geo_two(r) = sqrt(geo(θ_r) × geo(θ_r_inv))

is the geometric mean of forward and reverse winding couplings.
This IS the double helix coupling — two simultaneous windings, one forward
(geo_r) and one reverse (geo_r_inv), combined as geometric mean.

For charm (residue 23, angle 552°):
  geo_two(23) = sqrt(geo(552°) × geo(408°))
              = sqrt(0.98907 × 0.16543)
              = 0.40451

The charm helicity suppression (Part I) is the double helix hitting the
120° SU(3) flip point: one strand completes, one is cut at half amplitude.
Survival = (2/3) × geo_out + (1/6) × geo_ret = 0.68695.

For the pion (residue 29):
  Both strands wind to the same angle (456°) — constructive interference
  of constituent masses, destructive interference at the boundary binding.
  This is why the pion is nearly massless.

### 5. Open Problems for Part IV

1. **B0 geometric factor**: The same-angle winding interference amplitude
   for boundary mesons. Expected to be a ratio of geo values at adjacent
   angular steps. This closes the remaining 30% error on pion mass.

2. **f_K and f_eta**: Kaon and eta decay constants from non-boundary
   residue vortex stiffness. Same formula with geo(7) and geo(1) respectively.

3. **Heavy quarkonia**: J/psi, Upsilon decay constants from double helix
   at same-sheet residues. Should be clean (already ~2% MAPE on masses).

4. **Charm double helix constraint**: The flipped path is excluded by
   decoherence — only same-direction double helix is physical for charm
   formation from gluon fusion. This constrains the charm meson sector.

---

## Connection to Known Physics

The formula f_pi = sqrt(alpha) × Lambda × geo^(1/4) has a natural home
in the Ginzburg-Landau / superfluid framework:

- 3He-B superfluid: Goldstone modes are spin waves whose stiffness is
  the superfluid density at the vortex core [Zavjalov et al. 2016]
- Abrikosov vortex: coherence length ξ ~ 1/Lambda sets the core size,
  stiffness ~ sqrt(rho_s) where rho_s ~ alpha × Lambda^2
- QCD superfluid [Son 2002]: pion speed v^2 = f^2/chi_I where chi_I
  is the isospin susceptibility ~ alpha × geo(boundary) × Lambda^2
  => f ~ sqrt(alpha × geo_bdy) × Lambda (one GL step, gives 41.6 MeV)
  => f ~ sqrt(alpha) × Lambda × geo_bdy^(1/4) (two GL steps, gives 91.2 MeV)

The two-step GL derivation (order param then stiffness) is the correct
physical picture because the pion couples to the ORIENTATION of the
order parameter (Goldstone mode), not the amplitude (Higgs mode).
Orientation stiffness requires two square roots from the coupling.

---

## Parameter Summary

All of the following from just alpha_q = 0.848809 and Lambda = 217 MeV:

| Quantity | Prediction | Observed | Error |
|----------|-----------|----------|-------|
| alpha_baryon | 0.5659 | ~0.55-0.57 (lattice) | ~2% |
| C_hyp | 49.67 MeV | 73.4/4 = 18.4... | needs path correction |
| f_pi | 91.16 MeV | 92.4 MeV | -1.34% |
| N-Delta gap | ~293 MeV | 293.1 MeV | ~0% |
| Goldstone ID | exact | exact | 0% |

Current quark masses (m_u, m_d, m_s etc.) are PDG inputs, not free
parameters of this framework. They are independent experimental measurements.

---

*Code: mod30_baryon_ladder.py, mod30_comparison.py*
*See github.com/historyViper/Sage*
