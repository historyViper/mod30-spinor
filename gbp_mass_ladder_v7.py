#!/usr/bin/env python3
"""
GBP v7 Mass Ladder - RESIDUE-FREE TOPOLOGY-ONLY VERSION
=========================================================
This version ELIMINATES residues entirely!

The physics intuition:
- Topology k (1,2,3) = which sheet/toroid (T1, T2, T3)
- Generation = family separation via S2[gen]
- Mass comes from k-scaling + generation + boundary

Formula options to test:
1. mass = E_ref * S2[gen] * exp(-k/π) * (1 + boundary_scale(k))
2. mass = E_ref * S2[gen] * φ^(-k) * (1 + boundary_scale(k))
3. mass = E_ref * S2[gen] * k^(-α) * (1 + boundary_scale(k))
4. mass = E_ref * S2[gen] * (1 + boundary_scale(k))  [no k factor]

The key test: Does topology k alone explain the mass hierarchy?
"""

import math
from typing import Dict, Tuple
from collections import defaultdict

# ============================================================================
# CONSTANTS
# ============================================================================

PHI = (1 + math.sqrt(5)) / 2
GEO_B = math.sin(math.pi / 15) ** 2
ALPHA_IR = 0.848809
LU = GEO_B / ALPHA_IR

GEN_N = {'gen1': 4, 'gen2': 7, 'gen3': 2}

# ============================================================================
# PARTICLE DATABASE
# ============================================================================

PARTICLE_MASSES = {
    'Xi_cc++': 3621.4, 'Xi_cc+': 3518.94, 'Omega_cc+': 2695.2,
    'Lambda_c+': 2286.46, 'Xi_c+': 2467.71, 'Xi_c0': 2470.44,
    'Sigma_c++': 2453.97, 'Sigma_c+': 2452.65, 'Sigma_c0': 2453.75,
    'Omega_c0': 2674.4, 'Xi_c*+': 2645.53, 'Xi_c*0': 2646.33,
    'Sigma_c*++': 2520.2, 'Sigma_c*+': 2518.8, 'Sigma_c*0': 2517.5, 'Omega_c*0': 2765.9,
    'Lambda': 1115.683, 'Sigma+': 1189.37, 'Sigma0': 1192.642, 'Sigma-': 1197.449,
    'Xi0': 1314.86, 'Xi-': 1321.71, 'Omega-': 1672.45,
    'Lambda_b0': 5620.6, 'Xi_b-': 5797.0, 'Xi_b0': 5768.4,
    'Sigma_b+': 5811.0, 'Sigma_b0': 5813.4, 'Omega_b-': 6046.0,
}

PARTICLE_FAMILIES = {
    'Lambda_c+': 'gen1', 'Sigma_c++': 'gen1', 'Sigma_c+': 'gen1', 'Sigma_c0': 'gen1',
    'Sigma_c*++': 'gen1', 'Sigma_c*+': 'gen1', 'Sigma_c*0': 'gen1',
    'Xi_c+': 'gen2', 'Xi_c0': 'gen2', 'Xi_c*+': 'gen2', 'Xi_c*0': 'gen2',
    'Omega_c0': 'gen2', 'Omega_c*0': 'gen2',
    'Xi_cc++': 'gen3', 'Xi_cc+': 'gen3', 'Omega_cc+': 'gen3',
    'Lambda': 'gen1', 'Sigma+': 'gen1', 'Sigma0': 'gen1', 'Sigma-': 'gen1',
    'Xi0': 'gen2', 'Xi-': 'gen2', 'Omega-': 'gen2',
    'Lambda_b0': 'gen1', 'Sigma_b+': 'gen1', 'Sigma_b0': 'gen1',
    'Xi_b-': 'gen2', 'Xi_b0': 'gen2', 'Omega_b-': 'gen2',
}

PARTICLE_TOPOLOGY = {
    'Lambda_c+': 1, 'Sigma_c++': 1, 'Sigma_c+': 1, 'Sigma_c0': 1,
    'Xi_c+': 2, 'Xi_c0': 2, 'Omega_c0': 3,
    'Xi_c*+': 2, 'Xi_c*0': 2, 'Omega_c*0': 3,
    'Sigma_c*++': 1, 'Sigma_c*+': 1, 'Sigma_c*0': 1,
    'Xi_cc++': 2, 'Xi_cc+': 2, 'Omega_cc+': 3,
    'Lambda': 1, 'Sigma+': 1, 'Sigma0': 1, 'Sigma-': 1,
    'Xi0': 2, 'Xi-': 2, 'Omega-': 3,
    'Lambda_b0': 1, 'Sigma_b+': 1, 'Sigma_b0': 1,
    'Xi_b-': 2, 'Xi_b0': 2, 'Omega_b-': 3,
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def S2(gen: str) -> float:
    """Geometric transmission factor"""
    return math.sin(GEN_N[gen] * math.pi / 15) ** 2

def boundary_scale(k: int) -> float:
    """Boundary scaling: LU * φ^k"""
    return LU * (PHI ** k)

# ============================================================================
# K-SCALING FUNCTIONS (TOPOLOGY ONLY - NO RESIDUES)
# ============================================================================

def k_scaling_exp(k: int) -> float:
    """Option 1: exp(-k/π) - exponential decay by topology"""
    return math.exp(-k / math.pi)

def k_scaling_phi(k: int) -> float:
    """Option 2: φ^(-k) - golden ratio decay"""
    return PHI ** (-k)

def k_scaling_inv(k: int, alpha: float = 1.0) -> float:
    """Option 3: k^(-α) - inverse power law"""
    return k ** (-alpha)

def k_scaling_none(k: int) -> float:
    """Option 4: no extra k factor - topology only via boundary"""
    return 1.0

def k_scaling_linear(k: int) -> float:
    """Option 5: linear k scaling"""
    return k

def k_scaling_quad(k: int) -> float:
    """Option 6: quadratic k scaling"""
    return k ** 2

# ============================================================================
# MASS FORMULAS (RESIDUE-FREE)
# ============================================================================

def compute_mass_formula1(E_ref: float, gen: str, k: int) -> float:
    """Formula: E_ref * S2[gen] * exp(-k/π) * (1 + boundary_scale(k))"""
    return E_ref * S2(gen) * k_scaling_exp(k) * (1 + boundary_scale(k))

def compute_mass_formula2(E_ref: float, gen: str, k: int) -> float:
    """Formula: E_ref * S2[gen] * φ^(-k) * (1 + boundary_scale(k))"""
    return E_ref * S2(gen) * k_scaling_phi(k) * (1 + boundary_scale(k))

def compute_mass_formula3(E_ref: float, gen: str, k: int, alpha: float = 1.0) -> float:
    """Formula: E_ref * S2[gen] * k^(-α) * (1 + boundary_scale(k))"""
    return E_ref * S2(gen) * k_scaling_inv(k, alpha) * (1 + boundary_scale(k))

def compute_mass_formula4(E_ref: float, gen: str, k: int) -> float:
    """Formula: E_ref * S2[gen] * (1 + boundary_scale(k)) - no k factor"""
    return E_ref * S2(gen) * k_scaling_none(k) * (1 + boundary_scale(k))

# ============================================================================
# FITTING FUNCTIONS
# ============================================================================

def fit_formula(formula_func, use_boundary: bool = True, use_S2: bool = True, alpha: float = 1.0) -> Tuple[float, float, Dict]:
    """
    Fit E_ref to minimize MAPE for a given formula.
    Returns (E_ref, MAPE, predictions)
    """
    valid_particles = [p for p in PARTICLE_MASSES if p in PARTICLE_FAMILIES and p in PARTICLE_TOPOLOGY]
    
    best_E_ref = 1000.0
    best_mape = 100.0
    best_preds = {}
    
    for E_ref in range(500, 10000, 50):
        total_err = 0.0
        preds = {}
        
        for name in valid_particles:
            gen = PARTICLE_FAMILIES[name]
            k = PARTICLE_TOPOLOGY[name]
            exp_mass = PARTICLE_MASSES[name]
            
            # Compute base mass
            if formula_func.__name__ == 'compute_mass_formula3':
                mass = formula_func(E_ref, gen, k, alpha)
            else:
                mass = formula_func(E_ref, gen, k)
            
            # Apply S2 and boundary
            if not use_S2:
                mass = mass / S2(gen) if S2(gen) > 0 else 0
            
            if not use_boundary:
                boundary = boundary_scale(k)
                mass = mass / (1 + boundary) if (1 + boundary) > 0 else 0
            
            if mass > 0:
                mape = abs(mass - exp_mass) / exp_mass * 100
                total_err += mape
                preds[name] = mass
        
        mape = total_err / len(valid_particles)
        if mape < best_mape:
            best_mape = mape
            best_E_ref = E_ref
            best_preds = preds
    
    return best_E_ref, best_mape, best_preds


def test_all_formulas():
    """Test all k-scaling formulas"""
    print("=" * 70)
    print("GBP v7 MASS LADDER - RESIDUE-FREE TOPOLOGY-ONLY")
    print("=" * 70)
    print("\nTesting: Does topology k alone explain mass hierarchy?")
    print("-" * 70)
    
    results = {}
    
    # Formula 1: exp(-k/π)
    E_ref, mape, preds = fit_formula(compute_mass_formula1)
    results['exp(-k/π)'] = (E_ref, mape, preds)
    print(f"\n1. exp(-k/π): E_ref={E_ref}, MAPE={mape:.2f}%")
    
    # Formula 2: φ^(-k)
    E_ref, mape, preds = fit_formula(compute_mass_formula2)
    results['φ^(-k)'] = (E_ref, mape, preds)
    print(f"2. φ^(-k):    E_ref={E_ref}, MAPE={mape:.2f}%")
    
    # Formula 3: k^(-α) with different alpha
    for alpha in [0.5, 1.0, 1.5, 2.0]:
        E_ref, mape, preds = fit_formula(compute_mass_formula3, alpha=alpha)
        results[f'k^(-{alpha})'] = (E_ref, mape, preds)
        print(f"3. k^(-{alpha}):  E_ref={E_ref}, MAPE={mape:.2f}%")
    
    # Formula 4: no k factor
    E_ref, mape, preds = fit_formula(compute_mass_formula4)
    results['no k factor'] = (E_ref, mape, preds)
    print(f"4. no k factor: E_ref={E_ref}, MAPE={mape:.2f}%")
    
    return results


def show_predictions(results):
    """Show sample predictions for best formula"""
    print("\n" + "=" * 70)
    print("BEST FORMULA PREDICTIONS")
    print("=" * 70)
    
    # Find best
    best_name = min(results.keys(), key=lambda x: results[x][1])
    E_ref, mape, preds = results[best_name]
    
    print(f"\nBest: {best_name}")
    print(f"E_ref = {E_ref} MeV, MAPE = {mape:.2f}%")
    print("-" * 70)
    print(f"{'Particle':<12} {'Topology':<8} {'Family':<8} {'Exp (MeV)':<12} {'Pred (MeV)':<12} {'Err%'}")
    print("-" * 70)
    
    for name in sorted(preds.keys(), key=lambda x: PARTICLE_MASSES[x]):
        k = PARTICLE_TOPOLOGY[name]
        gen = PARTICLE_FAMILIES[name]
        exp_mass = PARTICLE_MASSES[name]
        pred_mass = preds[name]
        err = abs(pred_mass - exp_mass) / exp_mass * 100
        print(f"{name:<12} {k:<8} {gen:<8} {exp_mass:<12.2f} {pred_mass:<12.2f} {err:.2f}%")


def ablation_on_best(results):
    """Run ablation on best formula"""
    print("\n" + "=" * 70)
    print("ABLATION TESTS ON BEST FORMULA")
    print("=" * 70)
    
    # Find best formula
    best_name = min(results.keys(), key=lambda x: results[x][1])
    E_ref, _, _ = results[best_name]
    
    valid_particles = [p for p in PARTICLE_MASSES if p in PARTICLE_FAMILIES and p in PARTICLE_TOPOLOGY]
    
    # Determine which formula function
    if 'exp(-k/π)' in best_name:
        formula_func = compute_mass_formula1
    elif 'φ^(-k)' in best_name:
        formula_func = compute_mass_formula2
    elif 'k^(-' in best_name:
        alpha = float(best_name.split('k^(-')[1].rstrip(')'))
        formula_func = compute_mass_formula3
    else:
        formula_func = compute_mass_formula4
    
    def compute_mape_ablated(use_boundary: bool, use_S2: bool) -> float:
        total_err = 0.0
        for name in valid_particles:
            gen = PARTICLE_FAMILIES[name]
            k = PARTICLE_TOPOLOGY[name]
            exp_mass = PARTICLE_MASSES[name]
            
            if formula_func.__name__ == 'compute_mass_formula3':
                mass = formula_func(E_ref, gen, k, alpha if 'alpha' in dir() else 1.0)
            else:
                mass = formula_func(E_ref, gen, k)
            
            if not use_S2:
                mass = mass / S2(gen) if S2(gen) > 0 else 0
            
            if not use_boundary:
                boundary = boundary_scale(k)
                mass = mass / (1 + boundary) if (1 + boundary) > 0 else 0
            
            if mass > 0:
                total_err += abs(mass - exp_mass) / exp_mass * 100
        
        return total_err / len(valid_particles)
    
    baseline = compute_mape_ablated(True, True)
    no_boundary = compute_mape_ablated(False, True)
    no_S2 = compute_mape_ablated(True, False)
    both = compute_mape_ablated(False, False)
    
    print(f"\nBaseline (full): {baseline:.2f}%")
    print(f"Remove boundary: {no_boundary:.2f}% (+{no_boundary - baseline:.2f}%)")
    print(f"Remove S2:       {no_S2:.2f}% (+{no_S2 - baseline:.2f}%)")
    print(f"Remove both:     {both:.2f}% (+{both - baseline:.2f}%)")


def compare_generations():
    """Check if generation separation works"""
    print("\n" + "=" * 70)
    print("GENERATION SEPARATION TEST")
    print("=" * 70)
    
    # Find best formula
    E_ref, _, _ = min(results.values(), key=lambda x: x[1])
    
    gen_errors = defaultdict(list)
    
    for name in PARTICLE_MASSES:
        if name in PARTICLE_FAMILIES:
            gen = PARTICLE_FAMILIES[name]
            k = PARTICLE_TOPOLOGY[name]
            exp_mass = PARTICLE_MASSES[name]
            
            # Simple formula: E_ref * S2[gen] * (1 + boundary)
            mass = E_ref * S2(gen) * (1 + boundary_scale(k))
            
            if mass > 0:
                err = abs(mass - exp_mass) / exp_mass * 100
                gen_errors[gen].append(err)
    
    print("\nMAPE by generation:")
    for gen in sorted(gen_errors.keys()):
        errors = gen_errors[gen]
        avg = sum(errors) / len(errors)
        print(f"  {gen}: {avg:.2f}% (n={len(errors)} particles)")


if __name__ == '__main__':
    results = test_all_formulas()
    show_predictions(results)
    ablation_on_best(results)
    compare_generations()
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    best_name = min(results.keys(), key=lambda x: results[x][1])
    best_mape = results[best_name][1]
    
    if best_mape < 30:
        print(f"✓ {best_name} works well! MAPE={best_mape:.2f}%")
        print("  → Topology k provides meaningful mass hierarchy")
    elif best_mape < 50:
        print(f"△ {best_name} is OK. MAPE={best_mape:.2f}%")
        print("  → Topology helps but other factors needed")
    else:
        print(f"✗ All formulas weak. Best MAPE={best_mape:.2f}%")
        print("  → Residues or other structure needed")
    
    print("\n" + "=" * 70)