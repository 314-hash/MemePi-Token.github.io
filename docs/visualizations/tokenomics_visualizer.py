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

def plot_supply_dynamics():
    """Visualize token supply reduction over time"""
    initial_supply = 314159265359
    burn_rate = 0.02
    transactions = np.linspace(0, 1000, 1000)
    supply = initial_supply * (1 - burn_rate) ** transactions

    plt.figure(figsize=(10, 6))
    plt.plot(transactions, supply, 'b-', linewidth=2)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_billions))
    plt.title('MemePi Supply Dynamics Over Transactions')
    plt.xlabel('Number of Transactions (thousands)')
    plt.ylabel('Total Supply')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, 'supply_dynamics.svg'), format='svg', bbox_inches='tight')
    plt.close()

def plot_price_impact():
    """Visualize price impact function"""
    volume_to_liquidity = np.linspace(0, 5, 1000)
    k = np.pi/2
    impact = k * np.arctan(volume_to_liquidity)

    plt.figure(figsize=(10, 6))
    plt.plot(volume_to_liquidity, impact, 'r-', linewidth=2)
    plt.axhline(y=np.pi/2, color='g', linestyle='--', alpha=0.5, label='Maximum Impact (π/2)')
    plt.title('MemePi Price Impact Model')
    plt.xlabel('Transaction Volume / Liquidity Pool Size')
    plt.ylabel('Price Impact')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'price_impact.svg'), format='svg', bbox_inches='tight')
    plt.close()

def plot_governance_weight():
    """Visualize governance weight calculation"""
    balances = np.linspace(0, 1000000, 1000)
    holding_times = np.array([30, 90, 180, 365])  # days

    plt.figure(figsize=(10, 6))
    for time in holding_times:
        weight = balances * np.sqrt(time/np.pi)
        plt.plot(balances, weight, label=f'{time} days', linewidth=2)

    plt.title('MemePi Governance Weight by Balance and Holding Time')
    plt.xlabel('Token Balance')
    plt.ylabel('Voting Power')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'governance_weight.svg'), format='svg', bbox_inches='tight')
    plt.close()

def plot_burn_distribution():
    """Visualize cumulative burn effect"""
    transactions = np.linspace(0, 1000, 1000)
    initial_supply = 314159265359
    burn_rate = 0.02
    
    remaining_supply = initial_supply * (1 - burn_rate) ** transactions
    burned_amount = initial_supply - remaining_supply

    plt.figure(figsize=(10, 6))
    plt.stackplot(transactions, 
                 [remaining_supply, burned_amount],
                 labels=['Remaining Supply', 'Burned Tokens'],
                 colors=['#2ecc71', '#e74c3c'])
    
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_billions))
    plt.title('MemePi Token Distribution Over Time')
    plt.xlabel('Number of Transactions (thousands)')
    plt.ylabel('Token Amount')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'burn_distribution.svg'), format='svg', bbox_inches='tight')
    plt.close()

def plot_transaction_rate():
    """Visualize transaction rate limits"""
    hours = np.linspace(0, 24, 1000)
    max_tx_per_hour = 11.46
    tx_limit = np.minimum(hours * max_tx_per_hour, hours * 0 + 24 * max_tx_per_hour)

    plt.figure(figsize=(10, 6))
    plt.plot(hours, tx_limit, 'b-', linewidth=2)
    plt.fill_between(hours, tx_limit, alpha=0.2)
    plt.title('MemePi Maximum Transaction Rate')
    plt.xlabel('Time (hours)')
    plt.ylabel('Cumulative Transactions Allowed')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, 'transaction_rate.svg'), format='svg', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Generate all visualizations
    plot_supply_dynamics()
    plot_price_impact()
    plot_governance_weight()
    plot_burn_distribution()
    plot_transaction_rate()
