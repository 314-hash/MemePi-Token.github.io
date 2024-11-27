import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import os

# Create output directory if it doesn't exist
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def format_billions(x, pos):
    """Format large numbers in billions"""
    return f'{x/1e9:.1f}B'

def animate_supply_burn():
    """Animate the token supply reduction and burn process"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    initial_supply = 314159265359
    burn_rate = 0.02
    
    # Initialize plots
    transactions = np.linspace(0, 1000, 100)
    supply = initial_supply * np.ones_like(transactions)
    burned = np.zeros_like(transactions)
    line1, = ax1.plot([], [], 'b-', linewidth=2)
    stack = ax2.stackplot([], [], labels=['Remaining Supply', 'Burned Tokens'],
                         colors=['#2ecc71', '#e74c3c'])
    
    def init():
        ax1.set_xlim(0, 1000)
        ax1.set_ylim(0, initial_supply * 1.1)
        ax2.set_xlim(0, 1000)
        ax2.set_ylim(0, initial_supply * 1.1)
        return line1, stack
    
    def animate(frame):
        current_supply = initial_supply * (1 - burn_rate) ** (transactions * frame/100)
        current_burned = initial_supply - current_supply
        
        line1.set_data(transactions, current_supply)
        
        # Update stackplot
        ax2.clear()
        ax2.stackplot(transactions, [current_supply, current_burned],
                     labels=['Remaining Supply', 'Burned Tokens'],
                     colors=['#2ecc71', '#e74c3c'])
        
        # Update labels and formatting
        ax1.set_title('MemePi Supply Dynamics')
        ax1.set_xlabel('Number of Transactions (thousands)')
        ax1.set_ylabel('Total Supply')
        ax1.yaxis.set_major_formatter(FuncFormatter(format_billions))
        ax1.grid(True, alpha=0.3)
        
        ax2.set_title('Token Distribution')
        ax2.set_xlabel('Number of Transactions (thousands)')
        ax2.set_ylabel('Token Amount')
        ax2.yaxis.set_major_formatter(FuncFormatter(format_billions))
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        return line1, stack
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100,
                                 interval=50, blit=True)
    anim.save(os.path.join(output_dir, 'supply_burn_animation.gif'),
             writer='pillow', fps=20)
    plt.close()

def animate_price_impact():
    """Animate the price impact function with varying transaction sizes"""
    fig, ax = plt.subplots(figsize=(10, 6))
    volume_to_liquidity = np.linspace(0, 5, 1000)
    k = np.pi/2
    impact = k * np.arctan(volume_to_liquidity)
    
    line, = ax.plot([], [], 'r-', linewidth=2, alpha=0.3)
    point, = ax.plot([], [], 'bo', markersize=10)
    max_line = ax.axhline(y=np.pi/2, color='g', linestyle='--', alpha=0.5,
                         label='Maximum Impact (π/2)')
    
    def init():
        line.set_data([], [])
        point.set_data([], [])
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 2)
        return line, point, max_line
    
    def animate(frame):
        current_volume = frame * 5 / 100
        current_impact = k * np.arctan(current_volume)
        
        line.set_data(volume_to_liquidity, impact)
        point.set_data([current_volume], [current_impact])
        
        ax.set_title('MemePi Price Impact Model')
        ax.set_xlabel('Transaction Volume / Liquidity Pool Size')
        ax.set_ylabel('Price Impact')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return line, point, max_line
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100,
                                 interval=50, blit=True)
    anim.save(os.path.join(output_dir, 'price_impact_animation.gif'),
             writer='pillow', fps=20)
    plt.close()

def animate_governance_weight():
    """Animate governance weight changes over time"""
    fig, ax = plt.subplots(figsize=(10, 6))
    balances = np.linspace(0, 1000000, 1000)
    line, = ax.plot([], [], 'b-', linewidth=2)
    
    def init():
        line.set_data([], [])
        ax.set_xlim(0, 1000000)
        ax.set_ylim(0, 1000000)
        return (line,)
    
    def animate(frame):
        holding_time = frame * 365 / 100  # Animate up to 365 days
        weight = balances * np.sqrt(holding_time/np.pi)
        
        line.set_data(balances, weight)
        
        ax.set_title(f'MemePi Governance Weight (Holding Time: {holding_time:.1f} days)')
        ax.set_xlabel('Token Balance')
        ax.set_ylabel('Voting Power')
        ax.grid(True, alpha=0.3)
        
        return (line,)
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100,
                                 interval=50, blit=True)
    anim.save(os.path.join(output_dir, 'governance_weight_animation.gif'),
             writer='pillow', fps=20)
    plt.close()

def animate_transaction_rate():
    """Animate transaction rate limits over a day"""
    fig, ax = plt.subplots(figsize=(10, 6))
    hours = np.linspace(0, 24, 1000)
    max_tx_per_hour = 11.46
    
    line, = ax.plot([], [], 'b-', linewidth=2, alpha=0.3)
    point, = ax.plot([], [], 'ro', markersize=10)
    
    def init():
        line.set_data([], [])
        point.set_data([], [])
        ax.set_xlim(0, 24)
        ax.set_ylim(0, max_tx_per_hour * 24 * 1.1)
        return line, point
    
    def animate(frame):
        current_hour = frame * 24 / 100
        tx_limit = np.minimum(hours * max_tx_per_hour,
                            hours * 0 + 24 * max_tx_per_hour)
        current_limit = min(current_hour * max_tx_per_hour,
                          24 * max_tx_per_hour)
        
        line.set_data(hours, tx_limit)
        point.set_data([current_hour], [current_limit])
        
        ax.set_title(f'MemePi Transaction Rate (Hour: {current_hour:.1f})')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Cumulative Transactions Allowed')
        ax.grid(True, alpha=0.3)
        
        return line, point
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100,
                                 interval=50, blit=True)
    anim.save(os.path.join(output_dir, 'transaction_rate_animation.gif'),
             writer='pillow', fps=20)
    plt.close()

if __name__ == "__main__":
    print("Generating animations... This may take a few minutes.")
    
    print("1/4: Creating supply and burn animation...")
    animate_supply_burn()
    
    print("2/4: Creating price impact animation...")
    animate_price_impact()
    
    print("3/4: Creating governance weight animation...")
    animate_governance_weight()
    
    print("4/4: Creating transaction rate animation...")
    animate_transaction_rate()
    
    print("All animations have been generated in the visualizations directory!")
