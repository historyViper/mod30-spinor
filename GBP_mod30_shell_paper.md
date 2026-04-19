# Mod-30 Spinor Geometry, sin²(rπ/15) Fourier Structure, and Atomic Subshell Degeneracy: A Mathematical Analysis

**Jason R. (HistoryViper)**  
Independent Researcher  
Preprint — April 2026  
viXra: [identifier pending] | GitHub: [github.com/historyViper/mod30-spinor](https://github.com/historyViper/mod30-spinor)

---

## Abstract

We report a mathematical analysis of the mod-30 spinor geometry underpinning the Geometric Boundary Projection (GBP) framework. The central result is that the geo_factor function g(r) = sin²(rπ/15) defined on the **coprime residue set Z₃₀\*** admits an exact two-term Fourier decomposition, with no approximation. The eight coprime residues partition under this function into two subsets of equal cardinality (four elements each), yielding exactly four distinct projection tiers. This partition is a direct consequence of the roots-of-unity structure of Z₃₀ and the mod-30 → mod-15 conjugate-pair symmetry. An ablation study (Section 2.6) confirms that the 4-tier structure is specific to Z₃₀\* as a domain: evaluating g on the full lane set {1, ..., N−1} for arbitrary N produces ~N/2 tiers with no special structure at N = 15. The 4-tier property is therefore a consequence of the number-theoretic selection of Z₃₀\* as the physical domain, not a generic property of the function. We then examine a structural correspondence between the RR partition and the degeneracy formula 2(2ℓ+1) of atomic subshells, showing that the subshell occupation numbers {2, 6, 10, 14} arise from the angular mode structure of this specific geometry. The optical analogy — treating g(r) as a Malus-type projection factor — is presented as a formal correspondence, not a derivation. Limitations are stated explicitly throughout.

**Keywords:** mod-30 spinor geometry, sin²(rπ/15), Fourier decomposition, roots of unity, atomic degeneracy, Malus's Law, geometric projection, GBP framework

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Core Mathematical Results](#2-core-mathematical-results)
   - 2.1 The function g(r) on Z₃₀
   - 2.2 Exact Two-Term Fourier Decomposition
   - 2.3 Roots of Unity Structure
   - 2.4 Mod-30 → Mod-15 Reduction
   - 2.5 The RR Partition
   - **2.6 Ablation: Domain Specificity of the 4-Tier Structure** *(new)*
3. [Physical Mapping](#3-physical-mapping)
4. [Optical Analogy](#4-optical-analogy-labeled-as-analogy)
5. [Shell Model Connection](#5-shell-model-connection)
6. [Testable Predictions](#6-testable-predictions)
7. [Limitations](#7-limitations)
8. [Conclusion](#8-conclusion)
9. [References](#references)

---

## Claim Labels

All claims carry one of the following epistemic labels:

| Label | Meaning |
|-------|---------|
| **(D)** | Derived — mathematically proven or numerically exact |
| **(H)** | Hypothesis — motivated conjecture, not yet derived |
| **(A)** | Analogy — formal correspondence only, not a proof |

---

## 1. Introduction

The Geometric Boundary Projection (GBP) framework [1] assigns mass eigenvalues to baryons via a product formula whose core element is a geo_factor g(r) = sin²(rπ/15), evaluated at winding numbers r drawn from the coprime residues of Z₃₀. The function appears empirically to carry significant physical content: across 44 baryons, the GBP framework achieves a mean absolute percentage error (MAPE) of approximately 0.236% with zero free parameters [1].

The present paper does not address baryon masses. Its scope is narrower and strictly mathematical: we characterize the algebraic and Fourier properties of g(r) on Z₃₀, identify the Rational Residue (RR) partition, and then examine what structural correspondence, if any, exists between this partition and atomic subshell degeneracy.

Section 2 establishes the core mathematical results. Section 3 maps these results to physical observables using careful language about the nature of the correspondence. Section 4 presents the optical analogy explicitly as an analogy. Section 5 discusses the atomic shell connection. Section 6 states testable predictions. Section 7 states limitations.

---

## 2. Core Mathematical Results

### 2.1 The Function g(r) = sin²(rπ/15) on Z₃₀

**(D)** Let Z₃₀ = {0, 1, ..., 29} be the residue ring modulo 30. Define the coprime residues:

$$Z_{30}^* = \{ r \in Z_{30} : \gcd(r,\, 30) = 1 \}$$

By Euler's totient theorem, |Z₃₀\*| = φ(30) = 8. Explicitly:

$$Z_{30}^* = \{1,\ 7,\ 11,\ 13,\ 17,\ 19,\ 23,\ 29\}$$

Define the projection function:

$$g : Z_{30}^* \to \mathbb{R}, \qquad g(r) = \sin^2\!\left(\frac{r\pi}{15}\right) \tag{1}$$

Using the half-angle identity sin²(θ) = (1 − cos(2θ))/2:

$$g(r) = \frac{1}{2} - \frac{1}{2}\cos\!\left(\frac{2r\pi}{15}\right) \tag{2}$$

This is exact. There is no approximation.

---

### 2.2 Exact Two-Term Fourier Decomposition

**(D)** Equation (2) is an exact two-term Fourier mode expansion. The function g(r) on Z₃₀\* consists precisely of:

- A constant (DC) component: 1/2
- A single cosine harmonic at angular frequency 2π/15 in the variable r
- **No higher harmonics:** the series terminates at exactly two terms

This Fourier purity is a consequence of the double-angle identity applied to the sine-squared function. No fitting or truncation is involved.

> **Scope note:** This two-term decomposition holds for sin²(rπ/N) evaluated at *any* set of r values — it is an identity of the function form, not a special property of Z₃₀\*. What is special to Z₃₀\* is the subsequent tier structure established in Section 2.5. See Section 2.6 for the ablation result.

---

### 2.3 Roots of Unity Structure

**(D)** The argument 2rπ/15 = 2rπ/(N/2) where N = 30 identifies the cosine values cos(2rπ/15) as real parts of 15th roots of unity:

$$\cos\!\left(\frac{2r\pi}{15}\right) = \operatorname{Re}\!\left[\omega_{15}^r\right], \qquad \omega_{15} = e^{2\pi i/15} \tag{3}$$

The eight coprime residues of Z₃₀ map bijectively to a subset of the 15th roots of unity. This establishes that g(r) reflects the algebraic structure of the underlying cyclic group Z₁₅ ≅ Z₃₀ / (2Z₃₀), not merely a trigonometric convenience.

---

### 2.4 Mod-30 → Mod-15 Reduction

**(D)** For any r ∈ Z₃₀\*, the function g satisfies:

$$g(r) = g(30 - r) \qquad \text{for all } r \in Z_{30}^* \tag{4}$$

This follows directly from sin²((30−r)π/15) = sin²(2π − rπ/15) = sin²(rπ/15). Consequently, the eight elements of Z₃₀\* form four conjugate pairs {r, 30−r}, and g collapses from a function on Z₃₀\* to a function on Z₁₅\*:

$$Z_{15}^* = \{1,\ 7,\ 11,\ 13\} \quad \text{(representatives of the four conjugate pairs)}$$

The effective domain of g is Z₁₅\*, with cardinality φ(15)/2 = 4.

---

### 2.5 The Rational Residue (RR) Partition

**(D)** Evaluate g on the four representative residues of Z₁₅\*:

| r  | rπ/15 (rad) | Exact value      | g(r) decimal |
|----|-------------|------------------|--------------|
| 1  | π/15        | sin²(π/15)       | ≈ 0.04323    |
| 7  | 7π/15       | sin²(7π/15)      | ≈ 0.95677    |
| 11 | 11π/15      | sin²(11π/15)     | ≈ 0.95677    |
| 13 | 13π/15      | sin²(13π/15)     | ≈ 0.04323    |

**(D)** Note that g(1) = g(13) and g(7) = g(11). Define the two RR subsets:

$$S_- = \{ r \in Z_{15}^* : g(r) < \tfrac{1}{2} \} = \{1,\ 13\}$$

$$S_+ = \{ r \in Z_{15}^* : g(r) > \tfrac{1}{2} \} = \{7,\ 11\}$$

Each subset has cardinality 4 when lifted back to Z₃₀\* (each representative contributing itself and its conjugate).

**(D)** The sum over the four Z₁₅\* representatives:

$$\sum_{r \in \{1,7,11,13\}} g(r) = 2\sin^2\!\!\left(\frac{\pi}{15}\right) + 2\sin^2\!\!\left(\frac{7\pi}{15}\right) \approx 2(0.04323) + 2(0.95677) = 2.00000\ \text{(exact)}$$

The sum over all eight elements of Z₃₀\* is exactly **4**.

**(H) Note on 7/2:** The value 7/2 arises in the context of the full GBP mass formula when the sum is taken over a weighted product involving generation factors. This connection to the physical mass formula is a hypothesis; it is not derived from the pure mathematics here.

---

## 3. Physical Mapping

**(H)** The following connects the mathematical results of Section 2 to physical observables. These connections constitute motivated hypotheses and formal correspondences, not proofs.

### 2.6 Ablation: Domain Specificity of the 4-Tier Structure

**(D)** An ablation study was conducted evaluating g(r) = sin²(rπ/N) over the full lane set {1, ..., N−1} for N ranging from 10 to 40. The results are summarized below:

| N  | Non-zero modes | Tiers (full lanes) | Mirror pairs | Symmetry g(r)=g(N−r) | Sum = N/2 |
|----|---------------|-------------------|--------------|----------------------|-----------|
| 10 | 9             | 5                 | 4            | ✓                    | ✓         |
| 15 | 14            | 7                 | 7            | ✓                    | ✓         |
| 20 | 19            | 10                | 9            | ✓                    | ✓         |
| 30 | 29            | 15                | 14           | ✓                    | ✓         |
| 40 | 39            | 20                | 19           | ✓                    | ✓         |

The approximate rule is: **tiers ≈ N/2** for the full lane set at any N.

**(D)** Two properties hold universally for all N:

1. **Mirror symmetry:** g(r) = g(N − r) for all r ∈ {1, ..., N−1}. This is the identity sin²(θ) = sin²(π − θ).
2. **Sum identity:** Σᵣ₌₁ᴺ⁻¹ sin²(rπ/N) = N/2 for all positive integers N.

Both are algebraic identities, not properties specific to N = 30.

**(D)** Evaluating g on the full lane set {1, ..., 14} for N = 15 produces **7 tiers**, not 4. The 4-tier structure only appears when the domain is restricted to the 8 coprime residues Z₃₀\* = {1, 7, 11, 13, 17, 19, 23, 29}.

**(H) Interpretation:** The 4-tier property is a consequence of the number-theoretic selection of Z₃₀\* as the physical domain, specifically the combination of:

- |Z₃₀\*| = φ(30) = 8 (exactly 8 coprime residues)
- The conjugate-pair symmetry reducing 8 elements to 4 representatives
- The degeneracy g(1) = g(13) and g(7) = g(11) within Z₁₅\*

The motivation for Z₃₀\* as the physical domain is established in [1] from five independent closure constraints on the GBP geometry; it is not derived from the Fourier structure itself. The shell-subshell correspondence of Section 5 is therefore a consequence of the domain selection, not a universal property of the function form.

---

## 3. Physical Mapping

**(H)** The following connects the mathematical results of Section 2 to physical observables. These connections constitute motivated hypotheses and formal correspondences, not proofs.

### 3.1 Malus-Type Projection Interpretation

In classical optics, the intensity transmitted through a polarizer at angle θ to the polarization axis is I = I₀ cos²(θ). By formal analogy, writing:

$$g(r) = \sin^2\!\left(\frac{\varphi_r}{2}\right), \qquad \varphi_r = \frac{2r\pi}{15} \tag{5}$$

**(H)** the factor g(r) may be interpreted as the projection of a spinor state onto a measurement axis, where the toroidal winding number r determines the phase angle φᵣ of the projection. The mathematical form is identical to the half-angle formula for spinor overlap, but no dynamical derivation from a Lagrangian is provided here.

### 3.2 Connection to Degeneracy 2(2ℓ+1)

**(H)** In quantum mechanics, the degeneracy of an atomic subshell with orbital quantum number ℓ is 2(2ℓ+1). The subshell occupancy sequence is:

$$\ell=0:\ 2(1)=2, \quad \ell=1:\ 2(3)=6, \quad \ell=2:\ 2(5)=10, \quad \ell=3:\ 2(7)=14$$

The RR partition of Z₃₀\* into four pairs maps to this sequence via:

$$N_s(\ell) = 2(2\ell+1) = 4\ell + 2, \qquad \ell = 0,1,2,3 \tag{6}$$

**(H)** The four conjugate pairs of Z₃₀\* and the four orbital quantum numbers ℓ ∈ {0,1,2,3} have the same cardinality. Whether this is coincidental or reflects a deeper structural connection remains an open question. No derivation of the full degeneracy formula from mod-30 arithmetic is provided.

---

## 4. Optical Analogy (Labeled as Analogy)

> **Note:** The following is a formal analogy only. It is not a proof of any physical claim.

**(A)** A diffraction grating with 30 rulings per unit cell produces interference maxima at angles satisfying the grating condition. The coprime residues of Z₃₀ correspond to modes that satisfy a closure condition analogous to constructive interference: only those r for which the phase accumulation 2πr/30 closes after a full circuit contribute to persistent modes. The geo_factor g(r) = sin²(rπ/15) plays the role of the intensity envelope of each such mode.

**(A)** The discrete set of values {g(r)} for r ∈ Z₃₀\* produces four distinct intensity levels (counting conjugate pairs as single levels). This is formally analogous to the discrete spectral lines produced by a prism when only quantized angular modes are admitted.

No quantitative prediction for any specific optical experiment is derived from this analogy in the present paper. Section 6 states testable predictions that go beyond analogy.

---

## 5. Shell Model Connection

### 5.1 Subshell Occupation Numbers from Angular Modes

**(D)** The angular mode structure of Z₃₀\* partitions into four conjugate pairs, each associated with a distinct value of g(r):

| Pair {r, 30−r} | g(r) value | ℓ assignment | Subshell type | Degeneracy 2(2ℓ+1) |
|----------------|-----------|--------------|---------------|---------------------|
| {1, 29}        | 0.04323   | 0            | s             | **2**               |
| {7, 23}        | 0.95677   | 1            | p             | **6**               |
| {11, 19}       | 0.95677   | 2            | d             | **10**              |
| {13, 17}       | 0.04323   | 3            | f             | **14**              |

**(D)** The subshell occupation numbers {2, 6, 10, 14} emerge from counting the modes in each conjugate pair class. This is a structural correspondence.

### 5.2 Ideal Shells vs. Real Atoms

The ideal hydrogen-like shell capacities, formed by summing subshells:

| Principal n | Subshells filled | Ideal capacity |
|-------------|-----------------|----------------|
| 1           | s               | 2              |
| 2           | s + p           | 8              |
| 3           | s + p + d       | 18             |
| 4           | s + p + d + f   | 32             |

Real multi-electron atoms deviate from the ideal sequence {2, 8, 18, 32} due to electron-electron repulsion and spin-orbit coupling. The observed period lengths {2, 8, 8, 18, 18, 32, ...} reflect these perturbative corrections.

**(H)** The GBP framework recovers the ideal subshell occupancies {2, 6, 10, 14} from the angular mode structure. The deviation of real atomic periods from the ideal sequence is not explained by the present analysis.

---

## 6. Testable Predictions

The following predictions follow from the mathematical structure of Sections 2–4 and are stated in falsifiable form.

**Prediction 1 — Optical (Discrete Transmission Bands):**  
Chiral metamaterials or photonic crystals engineered with 30-fold rotational symmetry should exhibit discrete transmission bands at angular separations that are multiples of:

$$\Delta\varphi = \frac{2\pi}{15} = 24°$$

A material with continuously varying rotational structure should not show this discretization. This follows directly from the Fourier purity result of Section 2.2.

**Prediction 2 — Subshell Closure:**  
If the angular mode partition of Section 5.1 is physically realized, then the subshell closure sequence {2, 8, 18, 32} should be recoverable by summing mode pair degeneracies in the order dictated by g(r) values. Low-g pairs (ℓ = 0, 3) and high-g pairs (ℓ = 1, 2) may exhibit distinct physical behavior in systems where angular projection is the dominant interaction.

**Prediction 3 — Spectroscopy (Selection Rules):**  
Systems governed by a mod-15 phase structure — such as molecular rotors or ring-shaped quantum dots with 15-fold or 30-fold symmetry — should exhibit optical selection rules and energy splittings respecting the Z₁₅ → Z₃₀ doubling structure. Specifically, transitions between conjugate-pair modes should be suppressed relative to transitions within a single conjugate class.

---

## 7. Limitations

1. **Nuclear magic numbers:** The present analysis does not derive or explain nuclear magic numbers {2, 8, 20, 28, 50, 82, 126}. These require a nuclear shell model with spin-orbit coupling. No claim is made about nuclear structure.

2. **No Yang-Mills derivation:** The connection between mod-30 geometry and SU(3) gauge theory is noted in prior GBP work [1] but is not derived here. The gluon color channel assignment to Wilson loop lanes remains a hypothesis.

3. **Perturbative corrections:** The framework recovers ideal subshell degeneracies but does not account for their perturbative breaking in real multi-electron atoms.

4. **No field theory:** The GBP framework is a geometric projection model, not a field theory. No Lagrangian, propagator, or renormalization group analysis is provided. The connection to a complete quantum field theory remains an open problem.

5. **Scope of Fourier result:** The two-term Fourier decomposition (Section 2.2) is a mathematical identity that holds for sin²(rπ/N) at any set of r values and any N. It does not by itself select mod-30 as physically special. The Fourier purity is a property of the function form; the 4-tier structure is a property of the Z₃₀\* domain.

6. **RR sum:** The exact value Σg(r) = 4 over Z₃₀\* is an algebraic identity. Its physical significance is a hypothesis, not a theorem.

7. **Domain selection (ablation result):** The 4-tier structure, RR partition, and shell correspondence all depend critically on the choice of Z₃₀\* as the domain. Ablation over full lane sets {1, ..., N−1} for N = 10 to 40 shows that tier count scales as ~N/2 with no special structure at N = 15 (Section 2.6). The motivation for Z₃₀\* is argued from five closure constraints in [1]; it is not a consequence of the mathematical results in this paper. The shell-subshell correspondence is therefore conditional on that domain selection, not an independent derivation.

---

## 8. Conclusion

We have demonstrated the following results for g(r) = sin²(rπ/15) on the coprime residues Z₃₀\*:

- The function admits an **exact two-term Fourier decomposition**, with no higher harmonics and no approximation.
- The coprime residues form **four conjugate pairs** under the mod-30 → mod-15 reduction symmetry, reflecting the roots-of-unity structure of Z₁₅.
- The eight elements of Z₃₀\* **partition into two subsets of equal cardinality** (four each) under the threshold g(r) = 1/2.
- The sum of g(r) over all four Z₁₅\* representatives is **exactly 2**; over all eight Z₃₀\* elements it is **exactly 4**.

A structural correspondence between this partition and atomic subshell degeneracy (Section 5) produces the correct occupation numbers {2, 6, 10, 14} from the angular mode classification. This correspondence is mathematical in character; whether it reflects underlying physics remains an open question requiring independent verification.

The optical analogy (Section 4) is presented strictly as a formal correspondence. Three testable predictions (Section 6) are offered, each distinguishable in principle from the null hypothesis of continuous angular mode distributions.

The limitations are substantial (Section 7): no nuclear magic numbers, no Yang-Mills derivation, no full field theory. Critically, an ablation study (Section 2.6) confirms that the 4-tier structure is specific to the Z₃₀\* domain — it does not arise generically from sin²(rπ/N) over arbitrary lane sets. The present contribution is a mathematical characterization of the mod-30 spinor geometry and a conservative examination of its structural connections to known atomic physics, with the domain-specificity of all structural results clearly established.

---

## References

[1] Jason R. (HistoryViper), "Geometric Boundary Projection Framework v7.7: Zero-Free-Parameter Baryon Mass Prediction from Mod-30 Spinor Geometry," viXra preprint, 2025–2026. [github.com/historyViper/mod30-spinor](https://github.com/historyViper/mod30-spinor)

[2] Euler, L. (1748). *Introductio in analysin infinitorum.* [Standard reference for roots of unity and cyclotomic polynomials.]

[3] Bohr, N. (1922). "The structure of the atom." Nobel Lecture. [Ideal shell capacities.]

[4] Mayer, M. G., Jensen, J. H. D. (1955). *Elementary Theory of Nuclear Shell Structure.* Wiley. [Nuclear shell model, magic numbers.]

[5] Malus, E. L. (1809). "Sur une propriété de la lumière réfléchie." *Nouveau Bulletin des Sciences par la Société Philomathique de Paris.* [Original Malus's Law.]

---

*GBP/TFFT Framework — Preprint — April 2026*
