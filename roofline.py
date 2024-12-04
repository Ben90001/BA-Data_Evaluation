import matplotlib.pyplot as plt
import numpy as np

from value_calculations import *
from evaluate_results import n_max
dim =3
if __name__ == "__main__":
    arithmetic_intensity = np.linspace(0.01, 2, 100000)

    n_values = list(range(1,n_max+1))
    intensityValues = [getArithmeticIntnsity(n,dim) for n in n_values]
    roofline_of_n = [np.minimum(peak_performance, intensityValues[n-1]*peak_sustainable_bandwidth)for n in n_values]
    print("roofline_of_n: "+str(roofline_of_n))
    # Roofline model
    roofline = np.minimum(peak_performance, arithmetic_intensity*peak_sustainable_bandwidth)

    # Plotting
    plt.plot(arithmetic_intensity, roofline, label="Roofline Model", color='b')
    plt.scatter(intensityValues,roofline_of_n)
    plt.xscale('log')
    plt.yscale('log')

    for i, (intensityValues, roofline_of_n) in enumerate(zip(intensityValues, roofline_of_n)):
        plt.text(intensityValues, roofline_of_n, n_values[i], fontsize=9, ha='right', color='blue')


    # Labels and title
    plt.xlabel('Arithmetic Intensity (FLOPS/Byte)')
    plt.ylabel('Performance (FLOPS/s)')
    plt.title('Roofline Model')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    plt.show()

