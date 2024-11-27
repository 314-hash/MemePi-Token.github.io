# MemePi Tokenomics Visualizations

This directory contains visual representations of MemePi's mathematical relationships and tokenomics models, including both static and annotated versions with detailed mathematical formulas.

## Installation
```bash
pip install numpy matplotlib
```

## Visualization Types

### 1. Static Visualizations
Generate basic visualizations without annotations:
```bash
python static_visualizer.py
```

### 2. Annotated Visualizations
Generate visualizations with mathematical formulas and explanations:
```bash
python annotated_visualizer.py
```

### 3. Animated Visualizations (Experimental)
Generate animated versions of the visualizations:
```bash
python tokenomics_animator.py
```

## Mathematical Components Visualized

### 1. Supply Dynamics
- **Formula**: S(t) = S₀ × (1-b)^n(t)
- **Variables**:
  - S₀ = π × 10¹¹ (initial supply)
  - b = 0.02 (burn rate)
  - n(t) = transaction count
- **Files**: 
  - `supply_snapshot_*.png`: Static snapshots
  - `supply_snapshot_*_annotated.png`: With mathematical annotations

### 2. Price Impact Model
- **Formula**: I(v) = (π/2) × arctan(v/L)
- **Properties**:
  - Maximum impact: π/2
  - v: Transaction volume
  - L: Liquidity pool size
- **Files**:
  - `price_impact_*.png`: Static snapshots
  - `price_impact_*_annotated.png`: With mathematical annotations

### 3. Governance Weight
- **Formula**: VP(a,t) = Balance(a) × √(HoldingTime(a)/π)
- **Properties**:
  - Linear with balance
  - Square root of holding time
  - π-normalized time factor
- **Files**:
  - `governance_weight_*.png`: Static snapshots
  - `governance_weight_*_annotated.png`: With mathematical annotations

### 4. Transaction Rate Limits
- **Formulas**:
  - Rate = 1/(π×100) tx/s
  - Cooldown = π×100 seconds
  - Daily Maximum = 86400/(π×100) ≈ 275 tx
- **Files**:
  - `transaction_rate_*.png`: Static snapshots
  - `transaction_rate_*_annotated.png`: With mathematical annotations

## File Organization

```
visualizations/
├── static_visualizer.py         # Basic visualization generator
├── annotated_visualizer.py      # Generator with mathematical annotations
├── tokenomics_animator.py       # Animated visualization generator
├── *.png                        # Static snapshots
├── *_annotated.png             # Snapshots with mathematical formulas
└── *.svg                        # Vector graphics versions
```

## Usage Instructions

1. **Generate Basic Visualizations**:
   ```bash
   python static_visualizer.py
   ```
   This creates basic PNG snapshots of all tokenomics components.

2. **Generate Annotated Visualizations**:
   ```bash
   python annotated_visualizer.py
   ```
   This creates enhanced versions with mathematical formulas and explanations.

3. **Generate Animations** (if supported):
   ```bash
   python tokenomics_animator.py
   ```
   This attempts to create animated GIFs of the tokenomics in action.

## Mathematical Properties

1. **Supply Dynamics**:
   - Exponential decay pattern
   - Asymptotic approach to zero
   - π-based initial supply

2. **Price Impact**:
   - π/2 bounded maximum
   - Arctangent scaling
   - Liquidity-sensitive

3. **Governance**:
   - Time-weighted voting power
   - Square root holding bonus
   - π-normalized weights

4. **Transaction Limits**:
   - π-based rate limiting
   - Predictable cooldowns
   - Anti-bot protection

## Requirements
- Python 3.x
- NumPy
- Matplotlib

## Notes
- High-resolution PNG files are provided for easy viewing
- SVG files are available for vector graphics
- Annotated versions include LaTeX-formatted mathematical formulas
- Animation generation may be hardware-intensive
