import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Rectangle
import os

# Create output directory if it doesn't exist
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def format_billions(x, pos):
    """Format large numbers in billions"""
    return f'{x/1e9:.1f}B'

def add_math_box(ax, text, position='top'):
    """Add a box with mathematical formula"""
    if position == 'top':
        bbox = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8)
        ax.text(0.5, 0.98, text, transform=ax.transAxes, ha='center', va='top',
                bbox=bbox, fontsize=10)
    else:  # right
        bbox = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8)
        ax.text(0.98, 0.5, text, transform=ax.transAxes, ha='right', va='center',
                bbox=bbox, fontsize=10, rotation=0)

def create_supply_snapshots():
    """Create annotated snapshots of supply dynamics"""
    initial_supply = 314159265359
    burn_rate = 0.02
    
    snapshots = [0, 250, 500, 750, 1000]
    for frame in snapshots:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14))
        
        transactions = np.linspace(0, 1000, 100)
        supply = initial_supply * (1 - burn_rate) ** (transactions * frame/1000)
        burned = initial_supply - supply
        
        # Plot supply curve
        ax1.plot(transactions, supply, 'b-', linewidth=2)
        ax1.set_title(f'MemePi Supply Dynamics (Transaction Period: {frame})')
        ax1.set_xlabel('Number of Transactions (thousands)')
        ax1.set_ylabel('Total Supply')
        ax1.yaxis.set_major_formatter(FuncFormatter(format_billions))
        ax1.grid(True, alpha=0.3)
        
        # Add mathematical annotations
        supply_formula = (
            r"Supply Formula:"
            "\n"
            r"$S(t) = S_0 \times (1-b)^{n(t)}$"
            "\n"
            r"where:"
            "\n"
            r"$S_0 = \pi \times 10^{11}$"
            "\n"
            r"$b = 0.02$ (burn rate)"
            "\n"
            r"$n(t)$ = transaction count"
        )
        add_math_box(ax1, supply_formula, 'right')
        
        # Plot distribution
        ax2.stackplot(transactions, [supply, burned],
                     labels=['Remaining Supply', 'Burned Tokens'],
                     colors=['#2ecc71', '#e74c3c'])
        ax2.set_title('Token Distribution')
        ax2.set_xlabel('Number of Transactions (thousands)')
        ax2.set_ylabel('Token Amount')
        ax2.yaxis.set_major_formatter(FuncFormatter(format_billions))
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Add burn formula
        burn_formula = (
            r"Burn Amount per Transaction:"
            "\n"
            r"$B(t_i) = 0.02 \times V(t_i)$"
            "\n"
            r"Total Burned:"
            "\n"
            r"$B_{total}(t) = S_0 - S(t)$"
        )
        add_math_box(ax2, burn_formula, 'right')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'supply_snapshot_{frame}_annotated.png'),
                   dpi=300, bbox_inches='tight')
        plt.close()

def create_price_impact_snapshots():
    """Create annotated snapshots of price impact"""
    snapshots = [0, 1, 2, 3, 4]
    volume_to_liquidity = np.linspace(0, 5, 1000)
    k = np.pi/2
    impact = k * np.arctan(volume_to_liquidity)
    
    for current_volume in snapshots:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot full curve
        ax.plot(volume_to_liquidity, impact, 'r-', linewidth=2, alpha=0.3)
        
        # Plot current point
        current_impact = k * np.arctan(current_volume)
        ax.plot(current_volume, current_impact, 'bo', markersize=10)
        
        # Add reference line
        ax.axhline(y=np.pi/2, color='g', linestyle='--', alpha=0.5,
                  label='Maximum Impact (π/2)')
        
        ax.set_title(f'MemePi Price Impact Model (Volume/Liquidity: {current_volume})')
        ax.set_xlabel('Transaction Volume / Liquidity Pool Size')
        ax.set_ylabel('Price Impact')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add mathematical annotations
        impact_formula = (
            r"Price Impact Formula:"
            "\n"
            r"$I(v) = \frac{\pi}{2} \arctan(\frac{v}{L})$"
            "\n"
            r"where:"
            "\n"
            r"$v$ = transaction volume"
            "\n"
            r"$L$ = liquidity pool size"
            "\n"
            r"Maximum Impact: $\lim_{v \to \infty} I(v) = \frac{\pi}{2}$"
        )
        add_math_box(ax, impact_formula, 'right')
        
        plt.savefig(os.path.join(output_dir, f'price_impact_{current_volume}_annotated.png'),
                   dpi=300, bbox_inches='tight')
        plt.close()

def create_governance_snapshots():
    """Create annotated snapshots of governance weight"""
    balances = np.linspace(0, 1000000, 1000)
    holding_times = [30, 90, 180, 365]  # days
    
    for time in holding_times:
        fig, ax = plt.subplots(figsize=(12, 8))
        weight = balances * np.sqrt(time/np.pi)
        
        ax.plot(balances, weight, 'b-', linewidth=2)
        ax.set_title(f'MemePi Governance Weight (Holding Time: {time} days)')
        ax.set_xlabel('Token Balance')
        ax.set_ylabel('Voting Power')
        ax.grid(True, alpha=0.3)
        
        # Add mathematical annotations
        governance_formula = (
            r"Voting Power Formula:"
            "\n"
            r"$VP(a,t) = Balance(a) \times \sqrt{\frac{HoldingTime(a)}{\pi}}$"
            "\n"
            r"Properties:"
            "\n"
            r"1. Linear with balance"
            "\n"
            r"2. Square root of holding time"
            "\n"
            r"3. π-normalized time factor"
        )
        add_math_box(ax, governance_formula, 'right')
        
        plt.savefig(os.path.join(output_dir, f'governance_weight_{time}_annotated.png'),
                   dpi=300, bbox_inches='tight')
        plt.close()

def create_transaction_rate_snapshots():
    """Create annotated snapshots of transaction rate limits"""
    hours = np.linspace(0, 24, 1000)
    max_tx_per_hour = 11.46  # derived from π
    snapshots = [6, 12, 18, 24]  # hours
    
    for current_hour in snapshots:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Calculate limits
        tx_limit = np.minimum(hours * max_tx_per_hour,
                            hours * 0 + 24 * max_tx_per_hour)
        current_limit = min(current_hour * max_tx_per_hour,
                          24 * max_tx_per_hour)
        
        # Plot full curve and current point
        ax.plot(hours, tx_limit, 'b-', linewidth=2, alpha=0.3)
        ax.plot(current_hour, current_limit, 'ro', markersize=10)
        
        ax.set_title(f'MemePi Transaction Rate (Hour: {current_hour})')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Cumulative Transactions Allowed')
        ax.grid(True, alpha=0.3)
        
        # Add mathematical annotations
        rate_formula = (
            r"Transaction Rate Limits:"
            "\n"
            r"$Rate = \frac{1}{\pi \times 100}$ tx/s"
            "\n"
            r"$Cooldown = \pi \times 100$ seconds"
            "\n"
            r"Daily Limit:"
            "\n"
            r"$Max_{daily} = \frac{86400}{\pi \times 100} \approx 275$ tx"
        )
        add_math_box(ax, rate_formula, 'right')
        
        plt.savefig(os.path.join(output_dir, f'transaction_rate_{current_hour}_annotated.png'),
                   dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    print("Generating annotated visualization snapshots...")
    
    print("1/4: Creating annotated supply snapshots...")
    create_supply_snapshots()
    
    print("2/4: Creating annotated price impact snapshots...")
    create_price_impact_snapshots()
    
    print("3/4: Creating annotated governance weight snapshots...")
    create_governance_snapshots()
    
    print("4/4: Creating annotated transaction rate snapshots...")
    create_transaction_rate_snapshots()
    
    print("All annotated snapshots have been generated in the visualizations directory!")
