import matplotlib.pyplot as plt
import numpy as np


from value_calculations import *
from evaluate_results import *

#array of timeings -> array of performance for timings
def transform_time_to_performance(plotData,n__max): #3D only currently #SpMV only currently
    # return total work divided by total time
    performance = []
    for i in range(0,n_max):
        if plotData[i]== None:
            performance.append(np.nan)
        else:
            #print("valid value for performance calculation"+str(i))
            performance.append(getWork(i+1,dim=3)/(plotData[i]/1000000000)) # convert nanoseconds from data to secs

    return performance



dim =3
if __name__ == "__main__":
    arithmetic_intensity = np.linspace(0.0968, 0.0972, 100000)
    n_values = list(range(1,n_max+1))
    intensityValues = [getArithmeticIntnsity(n,dim,mtx_format) for n in n_values]
    roofline_of_n = [np.minimum(peak_performance, intensityValues[n-1]*peak_sustainable_bandwidth)for n in n_values]
    print("roofline_of_n: "+str(roofline_of_n))
    # [file][performances of n]
    SpMV_performances = [transform_time_to_performance(plotData3D[i][1],n_max) for i in range(0,len(plotData3D))]

    # Roofline model
    roofline = np.minimum(peak_performance, arithmetic_intensity*peak_sustainable_bandwidth)

    # Plotting
    plt.plot(arithmetic_intensity, roofline, label="Roofline Model", color='b')
    #plt.scatter(intensityValues,roofline_of_n)
    for SpMV_performance in SpMV_performances:
        plt.plot(intensityValues, SpMV_performance, label="a resutl")
    plt.xscale('log')
    plt.yscale('log')

    #for i, intensity in enumerate(intensityValues):
        #plt.axvline(x=intensity, color='blue', linestyle='--', linewidth=0.8)
        #plt.text(intensity, plt.ylim()[1] * 0.9, n_values[i], fontsize=9, ha='center', color='blue', rotation=90)


    # Labels and title
    plt.ylabel('Performance (FLOPS/s)')
    plt.xlabel('Arithmetic Intensity (FLOPS/Byte)')
    plt.title('Roofline Model - SpMV')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    plt.show()

