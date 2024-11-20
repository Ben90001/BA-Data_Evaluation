import numpy as np
import matplotlib.pyplot as plt

def plot_roofline(peak_flops, peak_mem_bw):
    # Define the range of operational intensity
    x = np.linspace(0, peak_mem_bw / 4, 100)  # Operational intensity (FLOPs/byte)
    
    # Roofline curves
    flops_line = np.minimum(peak_flops, peak_mem_bw * x)  # Memory bandwidth limit
    memory_line = np.full_like(x, peak_mem_bw)  # Peak memory bandwidth
    
    # Plotting the roofline
    plt.figure(figsize=(10, 6))
    plt.plot(x, flops_line, label='Roofline (FLOPs)', color='blue')
    plt.axhline(y=peak_mem_bw, color='red', linestyle='--', label='Peak Memory Bandwidth')
    
    # Labels and title
    #plt.xscale('log')
    #plt.yscale('log')
    #plt.xlim(1e-3, peak_mem_bw)
    #plt.ylim(1e-3, peak_flops * 2)
    plt.xlabel('Operational Intensity (FLOPs/Byte)')
    plt.ylabel('Performance (FLOPs)')
    plt.title('Roofline Model')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()

# Example values for peak performance
peak_flops = 1e12  # 1 TFLOP
peak_mem_bw = 49333333333  # 49,3 GB/s

plot_roofline(peak_flops, peak_mem_bw)

