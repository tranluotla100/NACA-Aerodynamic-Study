"""
COMPARING NACA 0012, 1408, 2408 FROM XFOIL DATA
"""
import matplotlib.pyplot as plt
import numpy as np

print("COMPARING NACA 0012, 1408, 2408 FROM XFOIL DATA")

airfoil_files = {
    "NACA 0012 (Symmetric)": "naca0012_results.txt",
    "NACA 1408 (1% camber)": "naca1408_results.txt", 
    "NACA 2408 (2% camber)": "naca2408_results.txt"
}

colors = {
    "NACA 0012 (Symmetric)": "blue",
    "NACA 1408 (1% camber)": "green",
    "NACA 2408 (2% camber)": "red"
}

all_data = {}

for name, filename in airfoil_files.items():
    angles = []
    cls = []
    cds = []
    
    print(f"\nReading {name} from {filename}...")
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if line and not line.startswith('-') and 'alpha' not in line.lower():
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        angle = float(parts[0])
                        cl = float(parts[1])
                        cd = float(parts[2])
                        
                        angles.append(angle)
                        cls.append(cl)
                        cds.append(cd)
                    except:
                        continue
        
        if angles:
            all_data[name] = {
                "angles": angles,
                "cl": cls,
                "cd": cds,
                "color": colors[name]
            }
            print(f"  ✓ Found {len(angles)} data points")
        else:
            print(f"  ⚠ No data found in {filename}")
            
    except FileNotFoundError:
        print(f"  ✗ {filename} not found")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

print("\n" + "=" * 30)
print(" AIRFOIL COMPARISON RESULTS")
print("=" * 30)

for name, data in all_data.items():
    ax1.plot(data["angles"], data["cl"], 
             marker='o', linestyle='-', linewidth=2,
             color=data["color"], label=name)
    
    if 0 in data["angles"]:
        idx = data["angles"].index(0)
        print(f"{name}: Cl at α=0° = {data['cl'][idx]:.4f}")
    
    if 5 in data["angles"]:
        idx = data["angles"].index(5)
        print(f"{name}: Cl at α=5° = {data['cl'][idx]:.4f}")

ax1.set_xlabel('Angle of Attack (degrees)')
ax1.set_ylabel('Lift Coefficient (Cl)')
ax1.set_title(' Comparison: Lift Curves')
ax1.grid(True, alpha=0.3)
ax1.legend()

for name, data in all_data.items():
    ax2.plot(data["angles"], data["cd"], 
             marker='s', linestyle='--', linewidth=2,
             color=data["color"], label=name)

ax2.set_xlabel('Angle of Attack (degrees)')
ax2.set_ylabel('Drag Coefficient (Cd)')
ax2.set_title(' Comparison: Drag Curves')
ax2.grid(True, alpha=0.3)

for name, data in all_data.items():
    if len(data["cl"]) == len(data["cd"]):
        ld_ratios = []
        for cl, cd in zip(data["cl"], data["cd"]):
            if cd > 0:
                ld_ratios.append(cl / cd)
            else:
                ld_ratios.append(0)
        
        if ld_ratios:
            best_ld = max(ld_ratios)
            best_idx = ld_ratios.index(best_ld)
            print(f"{name}: Best L/D = {best_ld:.1f} at α = {data['angles'][best_idx]}°")
        
        ax3.plot(data["angles"], ld_ratios,
                 marker='^', linestyle=':', linewidth=2,
                 color=data["color"], label=name)

ax3.set_xlabel('Angle of Attack (degrees)')
ax3.set_ylabel('Lift/Drag Ratio')
ax3.set_title('Comparison: Aerodynamic Efficiency')
ax3.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig('airfoil_comparison.png', dpi=150, bbox_inches='tight')
print(f"\n✓ Saved comparison plot as 'airfoil_comparison.png'")

with open('airfoil_summary.csv', 'w') as f:
    f.write('Airfoil,Cl_0deg,Cl_5deg,Best_L/D,Best_Angle\n')
    for name, data in all_data.items():
        cl_0 = cl_5 = best_ld = best_angle = 0
        
        if 0 in data["angles"]:
            idx = data["angles"].index(0)
            cl_0 = data["cl"][idx]
        
        if 5 in data["angles"]:
            idx = data["angles"].index(5)
            cl_5 = data["cl"][idx]
        
        if len(data["cl"]) == len(data["cd"]):
            ld_ratios = []
            for cl, cd in zip(data["cl"], data["cd"]):
                if cd > 0:
                    ld_ratios.append(cl / cd)
                else:
                    ld_ratios.append(0)
            
            if ld_ratios:
                best_ld = max(ld_ratios)
                best_idx = ld_ratios.index(best_ld)
                best_angle = data["angles"][best_idx]
        
        f.write(f'{name},{cl_0:.4f},{cl_5:.4f},{best_ld:.1f},{best_angle}\n')

print("✓ Saved summary as 'airfoil_summary.csv'")

plt.show()