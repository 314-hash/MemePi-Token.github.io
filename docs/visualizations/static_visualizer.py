import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

# Create output directory if it doesn't exist
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def format_billions(x, pos):
    """Format large numbers in billions"""
    return f'{x/1e9:.1f}B'

def create_supply_snapshots():
    """Create snapshots of supply dynamics at different points"""
    initial_supply = 314159265359
    burn_rate = 0.02
    
    # Create snapshots at different points
    snapshots = [0, 250, 500, 750, 1000]
    for frame in snapshots:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
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
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'supply_snapshot_{frame}.png'))
        plt.close()

def create_price_impact_snapshots():
    """Create snapshots of price impact at different points"""
    snapshots = [0, 1, 2, 3, 4]
    volume_to_liquidity = np.linspace(0, 5, 1000)
    k = np.pi/2
    impact = k * np.arctan(volume_to_liquidity)
    
    for current_volume in snapshots:
        fig, ax = plt.subplots(figsize=(10, 6))
        
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
        
        plt.savefig(os.path.join(output_dir, f'price_impact_{current_volume}.png'))
        plt.close()

def create_governance_snapshots():
    """Create snapshots of governance weight at different holding times"""
    balances = np.linspace(0, 1000000, 1000)
    holding_times = [30, 90, 180, 365]  # days
    
    for time in holding_times:
        fig, ax = plt.subplots(figsize=(10, 6))
        weight = balances * np.sqrt(time/np.pi)
        
        ax.plot(balances, weight, 'b-', linewidth=2)
        ax.set_title(f'MemePi Governance Weight (Holding Time: {time} days)')
        ax.set_xlabel('Token Balance')
        ax.set_ylabel('Voting Power')
        ax.grid(True, alpha=0.3)
        
        plt.savefig(os.path.join(output_dir, f'governance_weight_{time}.png'))
        plt.close()

def create_transaction_rate_snapshots():
    """Create snapshots of transaction rate limits at different hours"""
    hours = np.linspace(0, 24, 1000)
    max_tx_per_hour = 11.46
    snapshots = [6, 12, 18, 24]  # hours
    
    for current_hour in snapshots:
        fig, ax = plt.subplots(figsize=(10, 6))
        
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
        
        plt.savefig(os.path.join(output_dir, f'transaction_rate_{current_hour}.png'))
        plt.close()

if __name__ == "__main__":
    print("Generating visualization snapshots...")
    
    print("1/4: Creating supply snapshots...")
    create_supply_snapshots()
    
    print("2/4: Creating price impact snapshots...")
    create_price_impact_snapshots()
    
    print("3/4: Creating governance weight snapshots...")
    create_governance_snapshots()
    
    print("4/4: Creating transaction rate snapshots...")
    create_transaction_rate_snapshots()
    
    print("All snapshots have been generated in the visualizations directory!")
