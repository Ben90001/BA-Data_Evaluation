import matplotlib.pyplot as plt
import os
import statistics
from collections import defaultdict

from value_calculations import *


# 1. Retrieve data from files & process(e.g. average) them
# 2. transform data for each file in 4 plotable parts: 2D_Gen,2D_SpMV,3D_Gen,3D_SpMV
# 3. sort them into respective plots & decide which ones to plot

def getRawData(filename):
    # import data
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Split each line into integers and store them as a list
            row = list(map(int, line.split()))
            data.append(row)
    print(filename+": Data size: "+str(len(data)))
    return data
def getData(filename, data_type):
    data = getRawData(filename)
    #(n,dim) -> tuple-list of values
    map = defaultdict(list)
    for n, dim, round, gen_time, spmv_time in data: map[(n, dim)].append((gen_time, spmv_time))

    processedValues2D = []
    processedValues3D = []

    for (n, dim), values in map.items():
        gen_times = [v[0] for v in values]
        SpMV_times = [v[1] for v in values]
        processedValue = []
        if(data_type == "average"):
            processedValue = [n,dim, statistics.mean(gen_times), statistics.mean(SpMV_times)]
        elif(data_type == "median"):
            processedValue = [n,dim, statistics.median(gen_times), statistics.median(SpMV_times)]
        elif(data_type == "max"):
            processedValue = [n,dim, max(gen_times), max(SpMV_times)]
        elif(data_type == "min"):
            processedValue = [n,dim, min(gen_times), min(SpMV_times)]
        else:
            raise ValueError("data_type not not known")
        if dim == 2:
            processedValues2D.append(processedValue)
        elif dim == 3:
            processedValues3D.append(processedValue)
    
    processedValues2D.sort(key=lambda x: x[0])
    processedValues3D.sort(key=lambda x: x[0])
    print(filename+": Processed data size: "+ str(len(processedValues2D))+" and "+ str(len(processedValues3D)))
    print('\n')
    return (processedValues2D,processedValues3D)

def getDevisors(dim, n_upperBound, plot_per_devisor):
    if(plot_per_devisor=="no"):
        return [1]*(n_upperBound+1)
    devisors = list(range(0, n_upperBound+1))
    if(plot_per_devisor=="nnz"):
        for n in range(1, n_upperBound+1):
            devisors[n]= getNNZ(dim, n)
        return devisors
    if(plot_per_devisor=="N"):
        for n in range(1, n_upperBound+1):
            devisors[n]= pow(n,dim)
        return devisors
    raise ValueError(f"Invalid value for: {dim}")

#   data [x][0] = n
#   data [x][1] = dim
#   data [x][2] = gen_time
#   data [x][3] = SpMV_time
# returns plotable y-values: 2D_Gen,2D_SpMV,3D_Gen,3D_SpMV
def getPlotData(data,devisors,n_max):
    SpMV_data = []
    gen_data = []

    #index of next datapoint
    i=0 
    # ignoring all datapoints below plotstart
    while(data[i][0]< plotStartingPoint_n and i+1<len(data)):i+=1

    for n in range(1,n_max+1):
        if n == data[i][0]:
            SpMV_data.append(data[i][2]/devisors[n])
            gen_data.append(data[i][3]/devisors[n])
            if(i+1<len(data)): i+=1
        else:
            SpMV_data.append(None)
            gen_data.append(None)
    return [SpMV_data,gen_data]
def getRooflinePlot(dim, n_values,devisors,plotStartingPoint_n):
    result = []
    for n in n_values:
        value = None
        if n >= plotStartingPoint_n:
            value = (getWork(n,dim)/(1000000000*getRooflineValue(peak_performance,peak_sustainable_bandwidth, n, dim)))/ devisors[n]
        result.append(value)
    return result

def getXValues(dim,n_values,measuring_unit_x):
    x = n_values [:] # shallow copy
    if(measuring_unit_x == "n"):
        return x
    if(measuring_unit_x == "mtx in Bytes"):
        for n in range(0,n_max):
            x[n] = getNNZ(dim,n+1) * 8
        return x
    if(measuring_unit_x == "mtx+vec in Bytes"):
        for n in range(0,n_max):
            x[n] = (getNNZ(dim,n+1) + pow(n+1,dim)) * 8
        return x
    if(measuring_unit_x == "mtx+2vec in Bytes"):
        for n in range(0,n_max):
            x[n] = (getNNZ(dim,n+1) + 2*pow(n+1,dim)) * 8
        return x
    

# config
#-----------------------------------------------------------------------------------------------------------------------------

folder_string = "./results/400-4/"
plotStartingPoint_n = 15

plot_istl = True
plot_gko = True
plot_roofline = False

# executor
plot_ref = True
plot_omp = False
plot_cuda = True

# assembly data structure
plot_cpu = True
plot_gpu = True

# different matrix formats (gko,mtx_data)
plot_csr = True
plot_ell = True
plot_coo = False
plot_sellp = True

# ISTL BuildModes
plot_implicit = True
plot_row_wise = False

# special data
plot_No2 = False
plot_minor_deviations = False

plot_cache_sizes = True
plot_L1 = False
plot_L2 = True
plot_L3 = True
plot_RAM_size = False

# x-axis
# possible values: "n", "mtx+vec in Bytes" "mtx in Bytes"
measuring_unit_x = "mtx in Bytes"
# y-axis 
# possible values: "no","nnz","N"
plot_per_devisor = "nnz"
# possible values: "average" "median" "max" "min"
data_type = "min" 

plot_y_log = True
plot_x_log = True
plot_marker = False



plot_SpMV_d3_only = False
#-----------------------------------------------------------------------------------------------------------------------------

# Kib -> B
L1_size_byte = 32 * 1024 /8    # additional 32 for instructions
L2_size_byte = 512 * 1024 /8
L3_size_byte = 32768 * 1024 /8 # = 32MiB
RAM_size_byte = 534359343104    # free -b | grep Mem | awk '{print $7}'

#extract n_upperBound and rounds
n_max, rounds = map(int, folder_string[len("./results/"):-1].split('-'))


print("nnz verification: ")
print("d=2, n = 100, nnz= "+str(getNNZ(2,100))) # should be 49 600
print("d=3, n = 100, nnz= "+str(getNNZ(3,100))) # should be 6 940 000
print("d=2, n = 101, nnz= "+str(getNNZ(2,101))) # should be 50 601
print("d=3, n = 101, nnz= "+str(getNNZ(3,101))) # should be 7 150 901


if __name__ == "__main__":
    # get file names (exclude folders and hidden files)
    filenames = [file \
                for file in os.listdir(folder_string) \
                if os.path.isfile(folder_string+file) and not file.startswith('.')]
    filenames.sort()

    # file -> processedData
    rawDatas= [getData(folder_string+file,data_type) for file in filenames]
    rawDatas2D = [file[0] for file in rawDatas]
    rawDatas3D = [file[1] for file in rawDatas]

    # processedData -> plotData
    n_values = list(range(1, n_max+1))
    print("n_values"+ str(n_values))
    x_3D = getXValues(3,n_values,measuring_unit_x)
    x_2D = getXValues(2,n_values,measuring_unit_x)
    devisors_2D = getDevisors(2,n_max,plot_per_devisor)
    devisors_3D = getDevisors(3,n_max,plot_per_devisor)

    plotData2D = [getPlotData(data,devisors_2D,n_max) for data in rawDatas2D]
    plotData3D = [getPlotData(data,devisors_3D,n_max) for data in rawDatas3D]
    for i in range(0,len(plotData3D)):
        print("plotData2D length: "+str(len(plotData2D[i][0]))+" "+str(len(plotData2D[i][1]))+" from file: "+filenames[i])
        print("plotData3D length: "+str(len(plotData3D[i][0]))+" "+str(len(plotData3D[i][1]))+" from file: "+filenames[i])

    print("Size of the last plotData3D: gen "+str(len(plotData3D[-1][0]))+" SpMV "+str(len(plotData3D[-1][1])))
    print("The last plotData3D: gen "+str(plotData3D[-1][0]))
    print("The last plotData3D: SpMV "+str(plotData3D[-1][1]))
    
    rooflineValues_2D= getRooflinePlot(2,n_values,devisors_2D,plotStartingPoint_n)
    rooflineValues_3D= getRooflinePlot(3,n_values,devisors_3D,plotStartingPoint_n)
 


    # Add Data to Plots
    figure, axis = plt.subplots(2, 2)
    name = "no name assigned"
    for file in range(0,len(filenames)):
        name = filenames[file][:-4]
        filename_components = name.split('_')
        if(filename_components[0]=="ISTL"):
            if not plot_istl: continue
            if (not plot_implicit and filename_components[1]=="implicit"): continue
            if (not plot_row_wise and filename_components[1]=="row"): continue

        if(filename_components[0] == "gko"): 
            if not plot_gko: continue
            if((not plot_cpu) and filename_components[1] == "cpu"): continue
            if((not plot_gpu) and filename_components[1] == "gpu"): continue

            if((not plot_ref) and filename_components[2] == "ref"): continue 
            if((not plot_omp) and filename_components[2] == "omp"): continue 
            if((not plot_cuda) and filename_components[2] == "cuda"): continue

            if((not plot_csr) and filename_components[3] == "csr"): continue  
            if((not plot_coo) and filename_components[3] == "coo"): continue 
            if((not plot_ell) and filename_components[3] == "ell"): continue  
            if((not plot_sellp) and filename_components[3] == "sellp"): continue  
            del filename_components[4:7]
        if(not plot_No2 and filename_components[-1]== "No2"): continue
        if(not plot_minor_deviations and filename_components[-1]!= "No2" and 4<len(filename_components)): continue

        name = '_'.join(filename_components)
        axis[0,0].plot(x_2D, plotData2D[file][0], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
        axis[1,0].plot(x_2D, plotData2D[file][1], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
        axis[0,1].plot(x_3D, plotData3D[file][0], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
        axis[1,1].plot(x_3D, plotData3D[file][1], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
    if plot_roofline:
        axis[1,0].plot(x_2D, rooflineValues_2D, label="roofline", color="black")
        axis[1,1].plot(x_3D, rooflineValues_3D, label="roofline", color="black")

    # Set titles
    perDiv=""
    if(plot_per_devisor=="nnz"): perDiv= " per NNZ"
    if(plot_per_devisor=="N"): perDiv= " per N"
    axis[0,0].set_title("d=2 "+data_type+" time to generate sparse matrix"+perDiv)
    axis[1,0].set_title("d=2 "+data_type+" time to calculate SpMV"+perDiv)
    axis[0,1].set_title("d=3 "+data_type+" time to generate sparse matrix"+perDiv)
    axis[1,1].set_title("d=3 "+data_type+" time to calculate SpMV"+perDiv)


    for ax in axis.flat:
        ax.set_xlabel(measuring_unit_x)
        ax.set_ylabel('time in nanoseconds')
        if(plot_y_log): ax.set_yscale('log')
        if(plot_x_log): ax.set_xscale('log')
        if(plot_cache_sizes):
            if plot_L1:
                ax.axvline(x=L1_size_byte, color="grey", linestyle=':')#, label="L1 Cache")
            if plot_L2:
                ax.axvline(x=L2_size_byte, color="grey", linestyle='-.')#,label="L2 Cache")
            if plot_L3:
                ax.axvline(x=L3_size_byte, color="grey", linestyle='--')#, label="L3 Cache")
        if(plot_RAM_size): ax.axvline(x=RAM_size_byte, color="grey", linestyle='-')
        ax.legend()

    if(not plot_SpMV_d3_only):
        plt.show()
