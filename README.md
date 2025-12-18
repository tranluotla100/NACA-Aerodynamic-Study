# Computational NACA Wing Aerodynamics Study

## Project Summary
Computational analysis comparing NACA 0012, 1408, and 2408 airfoils. Determined optimal aspect ratio (AR=10) considering aerodynamic efficiency vs structural weight.

## Results
-**Camber Effect:** Linear relationship: Each 1% camber adds ~0.115 Cl at zero angle
  - 0% camber (NACA 0012): Cl = 0.000 at α=0°
  - 1% camber (NACA 1408): Cl = 0.114 at α=0°
  - 2% camber (NACA 2408): Cl = 0.229 at α=0°
- **Best Airfoil:** NACA 2408 achieves highest L/D = 83.8 at α=5°
- **Optimal AR:** Aspect ratio 10 provides best trade-off between aerodynamic efficiency (L/D=25.5) and structural weight

## Results
![Airfoil Comparison](airfoil_comparison.png)
![Aspect Ratio Trade-off](wing_tradeoff.png)

## Tools Used
- **XFOIL** for 2D airfoil analysis
- **Python** for data processing and visualization
- **Aerodynamic Theory:** Lifting line, beam theory

## Files
- `*.py` - Python analysis scripts
- `*.txt` - Raw XFOIL data  
- `*.png` - Result plots
- `*.csv` - Excel chart
