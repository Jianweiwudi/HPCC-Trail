import matplotlib.pyplot as plt
import numpy as np

# Read data
times = []
rates = []

with open('test.txt', 'r') as file:
    for i, line in enumerate(file):
        if i >= 50:
            break
        time, rate = line.strip().split()
        times.append(float(time))
        rates.append(float(rate))

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Plot data on both subplots
ax1.plot(times, rates, 'b-', linewidth=2)
ax2.plot(times, rates, 'b-', linewidth=2)

# Set y-axis ranges
ax1.set_ylim(0, 105)    # Full range
ax2.set_ylim(24, 26)    # Compressed range for detail view

# Set titles and labels
fig.suptitle('Transmission Rate vs Time', fontsize=14)
ax1.set_title('Full Range View', fontsize=12)
ax2.set_title('Detailed View', fontsize=12)
ax2.set_xlabel('Time', fontsize=12)
ax1.set_ylabel('Rate (Gbps)', fontsize=12)
ax2.set_ylabel('Rate (Gbps)', fontsize=12)

# Add grid
ax1.grid(True, linestyle='--', alpha=0.7)
ax2.grid(True, linestyle='--', alpha=0.7)

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig('rate_vs_time.png', dpi=300, bbox_inches='tight')

# Show plot
plt.show()