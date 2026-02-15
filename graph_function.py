import numpy as np
import matplotlib.pyplot as plt

# Define the functions
def f1(n):
    """Calculate f(n) = n^2 / log(n)"""
    # Use base 10 logarithm (log10)
    return n**2 / np.log10(n)

def f2(n):
    """Calculate f(n) = n^2"""
    return n**2

# Generate n values (avoiding n <= 1 since log(1) = 0 and log(n<1) is negative)
n_values = np.linspace(1.1, 20, 500)

# Calculate f(n) for each n
f1_values = f1(n_values)
f2_values = f2(n_values)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(n_values, f1_values, 'b-', linewidth=2, label='f(n) = n²/log(n) - Kociemba')
plt.plot(n_values, f2_values, 'r-', linewidth=2, label='f(n) = n² - CFOP and Beginner')
plt.grid(True, alpha=0.3)
plt.xlabel('n', fontsize=12)
plt.ylabel('f(n)', fontsize=12)
plt.title('Theoretical Efficiency of Tested Algorithms', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)

# Add some styling
plt.xlim(left=1)
plt.ylim(bottom=0)

# Show the plot
plt.tight_layout()
plt.savefig('function_graph.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'function_graph.png'")
plt.show()
