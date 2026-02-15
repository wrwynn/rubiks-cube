import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def plot_curves():
    """
    Plot a quadratic curve compared to an exponential curve
    """
    # Generate n values
    n_values = np.linspace(0, 20, 500)
    
    # Calculate quadratic function: f(n) = n^2
    quadratic = n_values ** 2
    
    # Calculate exponential function: f(n) = e^n
    exponential = np.exp(n_values)
    
    # Create subplots: one for quadratic alone, one for comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left plot: Quadratic curve alone (shows true parabolic shape)
    ax1.plot(n_values, quadratic, 'b-', linewidth=2)
    ax1.set_xlabel('n', fontsize=12)
    ax1.set_ylabel('Operations', fontsize=12)
    ax1.set_title("Beginner's and CFOP: O(n²)", fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Right plot: Exponential curve only
    ax2.plot(n_values, exponential, 'r-', linewidth=2)
    ax2.set_xlabel('n', fontsize=12)
    ax2.set_ylabel('Operations', fontsize=12)
    ax2.set_title('Kociemba: O(eⁿ)', fontsize=14, fontweight='bold')
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.0e'))
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('quadratic_vs_exponential.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 'quadratic_vs_exponential.png'")
    
    # Display the plot
    plt.show()

if __name__ == "__main__":
    plot_curves()
