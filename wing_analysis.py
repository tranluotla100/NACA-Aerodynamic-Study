"""
3D WING ANALYSIS - Aspect Ratio Trade-offs
Converting 2D airfoil data to 3D wings
"""
import matplotlib.pyplot as plt
import numpy as np

print("=" * 30)
print("3D WING ANALYSIS - ASPECT RATIO TRADE-OFFS")
print("=" * 30)

best_airfoil = "NACA 2408 (2% camber)"
cl_design = 0.7720  # Cl at α=5° from my results
cd_2d = 0.00921     # Cd at α=5° from my results

print(f"Using {best_airfoil} as baseline")
print(f"Design point: Cl = {cl_design:.3f}, Cd_2d = {cd_2d:.5f} at α=5°")

aspect_ratios = [6, 8, 10, 12, 14]
print(f"\nStudying Aspect Ratios: {aspect_ratios}")

print("CONVERTING 2D TO 3D (Lifting Line Theory)")

e = 0.9

print("\nAR | Induced Drag | Total Cd | L/D Ratio | Rel. Weight")
print("-" * 30)

ld_ratios = []
wing_weights = []

for AR in aspect_ratios:
    # Induced drag
    cdi = cl_design**2 / (np.pi * AR * e)
    
    # Total drag
    cd_total = cd_2d + cdi
    
    # L/D ratio
    ld = cl_design / cd_total
    
    # Structural weight
    weight = AR**1.5
    
    ld_ratios.append(ld)
    wing_weights.append(weight)
    
    print(f"{AR:2} | {cdi:11.5f} | {cd_total:8.5f} | {ld:8.1f} | {weight:11.2f}")

print("\n" + "=" * 30)
print("FINDING OPTIMAL ASPECT RATIO")
print("=" * 30)

for i in range(1, len(aspect_ratios)):
    ld_improvement = (ld_ratios[i] - ld_ratios[i-1]) / ld_ratios[i-1] * 100
    weight_increase = (wing_weights[i] - wing_weights[i-1]) / wing_weights[i-1] * 100
    
    print(f"AR {aspect_ratios[i-1]}→{aspect_ratios[i]}:")
    print(f"  L/D increases by {ld_improvement:.1f}%")
    print(f"  Weight increases by {weight_increase:.1f}%")
    print(f"  Efficiency gain per weight: {ld_improvement/weight_increase:.3f}")

optimal_idx = 2  # AR=10 (typically)
print(f" OPTIMAL ASPECT RATIO: AR = {aspect_ratios[optimal_idx]}")
print(f"   L/D = {ld_ratios[optimal_idx]:.1f}")
print(f"   Relative Weight = {wing_weights[optimal_idx]:.2f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(aspect_ratios, ld_ratios, 'bo-', linewidth=3, markersize=10)
ax1.set_xlabel('Aspect Ratio (AR)')
ax1.set_ylabel('Lift/Drag Ratio (L/D)')
ax1.set_title('Aerodynamic Efficiency vs Aspect Ratio')
ax1.grid(True, alpha=0.3)

ax1.plot(aspect_ratios[optimal_idx], ld_ratios[optimal_idx], 
         'ro', markersize=15, markerfacecolor='none', markeredgewidth=3)
ax1.text(aspect_ratios[optimal_idx], ld_ratios[optimal_idx]-2, 
         f'Optimal\nAR={aspect_ratios[optimal_idx]}', 
         ha='center', fontweight='bold')

ax2.plot(aspect_ratios, wing_weights, 'ro-', linewidth=3, markersize=10)
ax2.set_xlabel('Aspect Ratio (AR)')
ax2.set_ylabel('Relative Structural Weight')
ax2.set_title('Structural Weight vs Aspect Ratio')
ax2.grid(True, alpha=0.3)

ax2.plot(aspect_ratios[optimal_idx], wing_weights[optimal_idx], 
         'bo', markersize=15, markerfacecolor='none', markeredgewidth=3)

plt.tight_layout()
plt.savefig('wing_tradeoff.png', dpi=150, bbox_inches='tight')

with open('wing_analysis.csv', 'w') as f:
    f.write('Aspect_Ratio,L/D_ratio,Relative_Weight\n')
    for i in range(len(aspect_ratios)):
        f.write(f'{aspect_ratios[i]},{ld_ratios[i]:.1f},{wing_weights[i]:.2f}\n')


print("\n" + "=" * 30)
print("Conclusion:")
print("=" * 30)
print("Higher AR wings are aerodynamically better but heavier.")
print(f"AR={aspect_ratios[optimal_idx]} provides the best trade-off for genral purpose avition.")



plt.show()
