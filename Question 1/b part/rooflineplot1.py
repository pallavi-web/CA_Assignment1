import numpy as np
import matplotlib.pyplot as plt

MAX_GFLOPS = 147.2  # System's theoretical peak GFLOPS

# Memory bandwidths (in GB/s) for various memory hierarchy levels
mem_bandwidths = {
    'L1 Cache': 275.237,
    'L2 Cache': 144.758,
    'L3 Cache': 69.443,
    'DRAM': 19.822
}

# Generate logarithmic range of Operational Intensity (FLOPs per byte)
oi_range = np.logspace(-2, 2, 100)

def compute_roofline_curve(bandwidth, intensity_values):
    """Calculate performance curve for a given bandwidth and intensity array."""
    return np.minimum(MAX_GFLOPS, bandwidth * intensity_values)

def plot_program_points():
    """Scatter real program points on the graph."""
    bytes_per_element = 8
    data_points = [
        # (Memory_Bytes, Execution_Time_in_s, Label, Color)
        (177743938767, 323.77, "Program 1", 'blue'),
        (8496762936, 56.06, "Program 2", 'red'),
        (839672098, 45.03, "Program 3", 'green'),
        (651957351, 33.77, "Program 4", 'orange')
    ]
    total_flops = 137438953477

    for mem_bytes, time_sec, label, color in data_points:
        oi = total_flops / (mem_bytes * bytes_per_element)
        perf = total_flops / (time_sec * 1e9)
        plt.scatter(oi, perf, s=100, color=color, label=label)

# PLOTTING THE ROOFLINE MODEL

plt.figure(figsize=(12, 8))
plt.title("Roofline Performance Model", fontsize=16)
plt.xlabel("Operational Intensity (FLOPs/Byte)", fontsize=14)
plt.ylabel("Achieved Performance (GFLOPs)", fontsize=14)
plt.xscale("log")
plt.yscale("log")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Plot the roofline for each memory level
for label, bw in mem_bandwidths.items():
    performance = compute_roofline_curve(bw, oi_range)
    plt.plot(oi_range, performance, linewidth=3, label=label)

# Plot peak performance line
plt.axhline(y=MAX_GFLOPS, linestyle='--', color='darkred', label=f"Peak Performance = {MAX_GFLOPS} GFLOPs")

# Plot real application performance points
plot_program_points()

# Display legend
plt.legend()
plt.tight_layout()
plt.show()
