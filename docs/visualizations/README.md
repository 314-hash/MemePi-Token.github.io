# MemePi Tokenomics Visualizations

This directory contains visual representations of MemePi's mathematical relationships and tokenomics models. Each visualization is generated using Python with matplotlib and saved as an SVG file for high quality rendering.

## Installation
```bash
pip install numpy matplotlib
```

## Generated Visualizations

### 1. Supply Dynamics (supply_dynamics.svg)
- Shows how the total token supply decreases over time due to the 2% burn rate
- X-axis: Number of transactions (in thousands)
- Y-axis: Total token supply (in billions)
- Demonstrates the asymptotic approach to zero supply

### 2. Price Impact Model (price_impact.svg)
- Visualizes how transaction size affects price impact
- X-axis: Transaction volume relative to liquidity pool size
- Y-axis: Price impact (bounded by π/2)
- Shows the non-linear relationship using arctangent function

### 3. Governance Weight (governance_weight.svg)
- Illustrates voting power based on balance and holding time
- X-axis: Token balance
- Y-axis: Voting power
- Multiple lines show different holding periods (30, 90, 180, 365 days)
- Demonstrates square root relationship with holding time

### 4. Burn Distribution (burn_distribution.svg)
- Stacked area chart showing remaining supply vs burned tokens
- X-axis: Number of transactions (in thousands)
- Y-axis: Token amount (in billions)
- Visualizes the gradual transition from circulating to burned supply

### 5. Transaction Rate Limits (transaction_rate.svg)
- Shows the maximum allowed transactions over time
- X-axis: Time (hours)
- Y-axis: Cumulative transactions allowed
- Demonstrates the π-based rate limiting mechanism

## Animated Visualizations

### 1. Supply and Burn Animation (supply_burn_animation.gif)
- Dynamic visualization of token supply reduction
- Real-time burn rate effects
- Split-view showing:
  - Supply curve over time
  - Burn distribution changes

### 2. Price Impact Animation (price_impact_animation.gif)
- Moving point showing transaction size effects
- Real-time price impact calculation
- Visual demonstration of π/2 boundary
- Smooth transition through volume ranges

### 3. Governance Weight Animation (governance_weight_animation.gif)
- Dynamic holding time progression
- Real-time voting power calculation
- Visual representation of time-weighted bonuses
- Year-long holding period demonstration

### 4. Transaction Rate Animation (transaction_rate_animation.gif)
- 24-hour cycle visualization
- Real-time transaction limit updates
- Dynamic rate limiting demonstration
- Visual anti-bot protection

## Animation Generation
Generate all animations using:
```bash
python tokenomics_animator.py
```

Note: Animation generation may take a few minutes due to the high-quality output and number of frames.

## Key Mathematical Properties Illustrated

1. **Supply Reduction**
   - Exponential decay pattern
   - Never reaches zero (asymptotic)
   - Predictable burn rate

2. **Price Protection**
   - Bounded impact (maximum π/2)
   - Non-linear scaling
   - Natural resistance to large trades

3. **Governance Fairness**
   - Balance-weighted voting
   - Time-weighted bonus
   - Square root scaling for holding time

4. **Anti-Bot Measures**
   - Clear transaction rate limits
   - π-based cooldown periods
   - Predictable daily maximums

## Usage
Run the Python script to generate all visualizations:
```bash
python tokenomics_visualizer.py
```

The script will create SVG files in the same directory, which can be used in documentation, presentations, or the website.
