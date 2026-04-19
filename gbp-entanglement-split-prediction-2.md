# GBP Framework Prediction: Entanglement Split Periodicity in T4 Double-Helix Photons

**Author:** Jason Richardson (HistoryViper)  
**Repository:** [github.com/historyViper/mod30-spinor](https://github.com/historyViper/mod30-spinor)  
**Date:** April 2026  
**Status:** Prediction — Testable, Falsifiable, Zero Free Parameters

---

## Abstract

The Geometric Boundary Projection (GBP) framework predicts that entangled photons produced from a T4 double-helix source will exhibit a periodic entanglement split as a function of prism orientation angle. The period is 72°, with a characteristic split of 72.36% / 27.64% at the magic angle of 72°. At 36° offset, the split becomes exactly 50/50. This paper provides the full geometric derivation from first principles: the mod-30 spinor residue system, the T4 double-helix construction, the 2:1 winding ratio, the 5-fold symmetry axis, and the projection formula sin²(rπ/15). The derivation uses zero free parameters.

---

## 1. Introduction

Standard quantum optics assumes that entangled photon pairs from SPDC split 50/50 at a properly calibrated beam splitter. However, experimental anomalies have been reported: non-50/50 splits that vary with crystal orientation, and a "golden ratio resonance" in hexagonally poled crystals. The GBP framework explains these anomalies as geometric properties of the T4 double-helix photon.

---

## 2. Derivation

### 2.1 The Mod-30 Spinor Residue System

**Postulate 1:** Physical states correspond to the 8 coprime residues modulo 30:

```
Z₃₀* = {1, 7, 11, 13, 17, 19, 23, 29}
```

These are the only winding numbers that close consistently on a toroidal surface with a spinor double cover (720° closure).

**Postulate 2:** The projection of a state onto a measurement axis is given by:

```
P(r) = sin²(rπ/15)
```

This is Malus's Law applied to spinor geometry. The factor π/15 comes from 180°/15 = 12° increments on the spinor circle.

### 2.2 The 8 Lanes and Their Projections

| Lane r | Angle (degrees) | sin²(rπ/15) | Value |
|--------|-----------------|-------------|-------|
| 1      | 12°             | sin²(12°)   | 0.04323 |
| 7      | 84°             | sin²(84°)   | 0.98907 |
| 11     | 132°            | sin²(132°) = sin²(48°) | 0.95677 |
| 13     | 156°            | sin²(156°) = sin²(24°) | 0.16544 |
| 17     | 204°            | sin²(204°) = sin²(24°) | 0.16544 |
| 19     | 228°            | sin²(228°) = sin²(48°) | 0.95677 |
| 23     | 276°            | sin²(276°) = sin²(84°) | 0.98907 |
| 29     | 348°            | sin²(348°) = sin²(12°) | 0.04323 |

Note the pairing structure: {1,29}, {7,23}, {11,19}, {13,17}.

### 2.3 The T4 Double-Helix Photon

**Postulate 3:** The T4 double-helix photon is constructed by combining two T1 Möbius photons with a 2:1 winding ratio.

- One helix winds twice for every single wind of the other
- The total structure has 5-fold symmetry because 30/6 = 5 (the beat between 2 and 1)
- The two helices correspond to two different lane pairs

**Derivation of the 2:1 ratio:**

Let helix A have winding number r_A, helix B have winding number r_B. For a 2:1 ratio:

```
r_A : r_B = 2 : 1
```

In the mod-30 system, the smallest such pair is r_A = 2, r_B = 1. But lanes must be coprime to 30. The 2:1 ratio appears in the HE21 mode of the T2 toroid, which has a 2:1 phase relationship. In lane terms, this corresponds to a difference of 6 lanes (since 30/5 = 6). The two helices are at lanes that differ by 6.

From the lane table, pairs differing by 6:

| Lane r | Lane r+6 | Difference |
|--------|----------|------------|
| 7      | 13       | 6          |
| 11     | 17       | 6          |
| 13     | 19       | 6          |
| 17     | 23       | 6          |

The natural choice for the double helix is {7,13} or {11,17}. Both give the same projection ratio because sin²(84°) and sin²(24°) appear.

### 2.4 Projection of the Double Helix

When the double helix is measured at an angle θ relative to its symmetry axis, each helix projects according to sin² of its half-angle.

For lane 7: full angle on spinor circle = 720° × 7/30 = 168°. Half of that is 84°. So sin²(rπ/15) = sin²(half the full angle).

For the pair {7,13} at θ = 0° aligned with the 7-axis:

- Projection of helix A (lane 7) = sin²(7π/15) = 0.98907
- Projection of helix B (lane 13) = sin²(13π/15) = sin²(24°) = 0.16544
- Ratio = 0.98907 / 0.16544 ≈ 6

The ratio ~6 is not φ². The double helix is not measured along its lane axes directly — it is measured at an angle that reveals the 5-fold symmetry.

### 2.5 The 5-Fold Symmetry and the Magic Angle

The mod-30 geometry contains 5-fold symmetry because 30/6 = 5. The 5-fold axis corresponds to a rotation of 72° (since 360°/5 = 72°).

When the prism is aligned at 72° relative to the crystal axis, the projection is the beat between the two helices.

Let the two helices have phases φ₁ and φ₂ with φ₂ = 2φ₁ (the 2:1 ratio). The combined projection is:

```
P_total(θ) = sin²(θ + φ₁) + sin²(θ + 2φ₁)
```

The split ratio is:

```
Split = sin²(θ + 2φ₁) / (sin²(θ + φ₁) + sin²(θ + 2φ₁))
```

When the two angles differ by 36° (pentagonal geometry), we get the golden ratio. Let:

```
θ + φ₁ = 36°
θ + 2φ₁ = 72°
```

Then φ₁ = 36°, θ = 0°. At this alignment:

```
Split = sin²(72°) / (sin²(36°) + sin²(72°))
```

Using the known identity sin²(36°) + sin²(72°) = 5/4 = 1.25:

```
Split_A = sin²(72°) / 1.25 = 0.9045085 / 1.25 = 0.7236068  →  72.36068%
Split_B = sin²(36°) / 1.25 = 0.3454915 / 1.25 = 0.2763932  →  27.63932%
```

The ratio is:

```
0.7236068 / 0.2763932 = φ² = 2.618034
```

Because sin²(72°) / sin²(36°) = φ² exactly.

### 2.6 The Periodicity

The 5-fold symmetry means that rotating the prism by 72° returns the same alignment. Therefore: **Period = 72°**.

At half-period (36° offset):

```
θ + φ₁ = 72°
θ + 2φ₁ = 108°
```

Since sin²(72°) = sin²(108°), both projections are equal → **split = 50/50**.

### 2.7 Summary of Derived Results

| Quantity | Derivation | Value |
|----------|------------|-------|
| Magic angle | 5-fold symmetry: 360°/5 | 72° |
| 50/50 crossing | Half of magic angle | 36° |
| Split at magic angle | sin²(72°)/(sin²(36°)+sin²(72°)) | 72.3607% |
| Split ratio | sin²(72°)/sin²(36°) | φ² = 2.618034 |
| Period | 5-fold symmetry | 72° |

All derived from:
- Mod-30 spinor residues
- 2:1 winding ratio of T4 double helix
- 5-fold symmetry from 30/6 = 5
- Projection formula P = sin²(rπ/15)

**Zero free parameters.**

---

## 3. The Prediction

### 3.1 Strongest Single Prediction

When a T4 double-helix photon source is aligned with a prism at a relative angle of 72° (the magic angle), the entanglement split will be:

> **Channel A: 72.3607% ± 0.5%**  
> **Channel B: 27.6393% ± 0.5%**

### 3.2 Full Periodic Pattern

| θ (degrees) | Expected Split (A/B) |
|-------------|----------------------|
| 0° (reference) | Variable (depends on initial alignment) |
| 36° | 50/50 |
| 72° | 72.36 / 27.64 |
| 108° | 50/50 |
| 144° | 27.64 / 72.36 (swap) |
| 180° | Same as 0° |
| 216° | Same as 72° |
| 252° | Same as 108° |
| 288° | Same as 144° |
| 324° | Same as 36° |
| 360° | Same as 0° |

### 3.3 Falsification Conditions

This prediction is falsifiable. It is **wrong** if:

*GBP is falsified if:*

- **F1:** No variation in split with prism angle (flat line)
- **F2:** The period of variation is not 72° (within ±2°)
- **F3:** At θ = 72°, the split is not 72.36/27.64 (within ±0.5% absolute)
- **F4:** At θ = 36°, the split is not 50/50 (within ±0.5% absolute)

*HE21 mode coupling (Mechanism B) is indicated instead of topological winding (Mechanism A) if:*

- **F5:** Period is 90° rather than 72° → 4-fold mode coupling symmetry, not 5-fold topological winding
- **F6:** Split ratio degrades with path length or temperature → phase-matching dependent, not topologically protected
- **F7:** 50/50 crossings occur at 45° intervals rather than 36° → Mechanism B, not Mechanism A

Both Mechanism A and Mechanism B are GBP predictions. F5–F7 distinguish which topology is realized, not whether GBP is correct.

---

## 4. Experimental Requirements

### 4.1 Source

- SPDC source with a hexagonally poled nonlinear crystal
- Tuned to the golden ratio resonance (as observed in 2018 paper)
- Output filtered for T4 double-helix states

### 4.2 Optics

- Collimator
- Polarizer (to ensure pure T4 states)
- Rotatable prism on precision rotation stage (0.1° resolution)

### 4.3 Detection

- Two single-photon counting modules
- Coincidence counting
- Sufficient integration time for 0.5% statistical error

### 4.4 Procedure

1. Align prism at arbitrary reference (θ = 0°)
2. Measure split for 60 seconds
3. Rotate by 5°, repeat
4. Continue from 0° to 360°
5. Plot split vs. θ
6. Identify period and verify 50/50 at 36° intervals
7. Verify 72.36/27.64 at 72° intervals

---

## 5. Prior Evidence

Independent observations consistent with this prediction:

1. Non-50/50 splits in SPDC vary with crystal orientation
2. Golden ratio resonance observed in hexagonally poled crystals
3. 72° periodicity has not been ruled out by existing data

This prediction unifies these observations.

### 5.5 Two GBP Mechanisms: Topological Winding vs Mode Coupling

Within the GBP framework, the T4 double-helix photon can be realized by two distinct mechanisms. Both are GBP constructs — no equivalent exists in the standard quantum optics literature, which contains no mod-30 spinor geometry, no toroid topology classification, and no HE21 treatment of entangled photon structure.

The two mechanisms are:

**Mechanism A — Topological winding (this paper):** The T4 state arises from a genuine 2:1 topological winding number locked by the mod-30 spinor geometry. The winding is conserved by topology, not phase-matching. This gives 5-fold symmetry (30/6 = 5) and a period of 72°.

**Mechanism B — HE21 mode coupling:** The T4 state arises from an HE21-type fiber mode with 2:1 phase winding driven by coherent mode coupling between two parametric processes — analogous to the two reciprocal lattice vectors in the Gatti (2018) hexagonal crystal. This gives 4-fold azimuthal symmetry and a period of 90°.

Both mechanisms produce the φ² split ratio. They are distinguished experimentally as follows:

#### 5.5.1 Symmetry Discriminator

| Mechanism | Symmetry | Predicted Period | 50/50 Crossings |
|-----------|----------|-----------------|-----------------|
| HE21 mode coupling (Mechanism B) | 4-fold | 90° | Every 45° |
| Topological winding (Mechanism A, this paper) | 5-fold | **72°** | Every 36° |

The Gatti (2018) experiment is consistent with Mechanism A: the hexagonal crystal lattice has 6-fold symmetry, but the two-process resonance condition selects a subgroup. Tuning the pump angle θ_p relative to the hexagonal symmetry axis is consistent with 5-fold selection, not 4-fold.

#### 5.5.2 Stability Discriminator

Mechanism B (mode coupling) is phase-matching dependent. The φ² split ratio should degrade with path length and temperature as coherence between the two parametric processes is lost.

Mechanism A (topological winding) is protected by winding number conservation. The φ² split ratio should be stable across path length and temperature variations.

#### 5.5.3 Summary

The φ² split ratio alone cannot distinguish the two mechanisms — both predict it. The discriminating tests are F5, F6, and F7 in the falsification conditions above. A 72° period with stable split ratio across path length confirms Mechanism A. A 90° period or degrading split ratio indicates Mechanism B. Either result is a GBP prediction — but they point to different underlying topology.

---

## 6. Conclusion

The GBP framework derives a precise, testable prediction for entangled photon experiments from first principles:

- **Period:** 72° (from 5-fold symmetry)
- **Split at 72°:** 72.3607% / 27.6393% (from sin²(72°)/sin²(36°) = φ²)
- **50/50 crossings:** Every 36°

Zero free parameters. Falsifiable with a tabletop experiment.

If confirmed, this provides experimental evidence for:

- The T4 double-helix photon
- The mod-30 spinor geometry
- The geometric quantization of entanglement

---

## 7. References

1. Richardson, J. (2026). GBP Framework v7.7. [github.com/historyViper/mod30-spinor](https://github.com/historyViper/mod30-spinor)
2. Richardson, J. (2026). The Higgs Field as Time-String Tension.
3. Richardson, J. (2026). Tensor Time: A 1D String Theory of Spacetime.
4. Gatti, A., et al. (2018). "Golden ratio entanglement in hexagonally poled nonlinear crystals." *Phys. Rev. A* 98, 053827.
5. Gatti, A., et al. (2018). "Golden Ratio Gain Enhancement in Coherently Coupled Parametric Processes." *Scientific Reports* 8, 11840.
6. Gatti, A. (2020). "Engineering multipartite entanglement in nonlinear photonic crystals." *Phys. Rev. A* 101, 053841.
7. Gatti, A., Brambilla, E., & Jedrkiewicz, O. (2021). "Engineering multipartite coupling in doubly pumped parametric down-conversion processes." *Phys. Rev. A* 103, 043720.
8. Gatti, A. (2021). "Multipartite spatial entanglement generated by concurrent nonlinear processes." *Phys. Rev. A* 104, 052430.

---

*This prediction is offered for experimental test. Results regardless of outcome are welcome.*
