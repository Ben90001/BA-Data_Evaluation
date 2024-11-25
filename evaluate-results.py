import matplotlib.pyplot as plt
import os
import statistics
from collections import defaultdict

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

    processedValues = []
    for (n, dim), values in map.items():
        gen_times = [v[0] for v in values]
        SpMV_times = [v[1] for v in values]
        if(data_type == "average"):
            processedValues.append([n,dim, statistics.mean(gen_times), statistics.mean(SpMV_times)])
        elif(data_type == "median"):
            processedValues.append([n,dim, statistics.median(gen_times), statistics.median(SpMV_times)])
        elif(data_type == "max"):
            processedValues.append([n,dim, max(gen_times), max(SpMV_times)])
        elif(data_type == "min"):
            processedValues.append([n,dim, min(gen_times), min(SpMV_times)])
        else:
            raise ValueError("data_type not not known")
    print(filename+": Processed data size: "+ str(len(processedValues)))
    print('\n')
    return processedValues

def getNNZ(dim, n):
    if(dim==2):
        #old : return 5*pow(n,dim) -2*n -2
        return 5*n*n - 4*n
    if(dim==3):
        #old : return 7*pow(n,dim) -2*n*n -2*n -2
        return 7*n*n*n - 6*n*n
    raise ValueError(f"Invalid value for: {dim}")
def getN(dim,n):    
    return pow(n,dim)


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

#returns plotable y-values: 2D_Gen,2D_SpMV,3D_Gen,3D_SpMV
def getPlotData(data,devisors_2D,devisors_3D,plotStartingPoint_n,n_upperBound):
    plotData = [ \
        [data[n-1][2]/devisors_2D[n] for n in range(plotStartingPoint_n, n_upperBound+1)], \
        [data[n-1][3]/devisors_2D[n] for n in range(plotStartingPoint_n, n_upperBound+1)], \
        [data[n_upperBound+n-1][2]/devisors_3D[n] for n in range(plotStartingPoint_n, n_upperBound+1)], \
        [data[n_upperBound+n-1][3]/devisors_3D[n] for n in range(plotStartingPoint_n, n_upperBound+1)] \
    ]
    return plotData

def getXValues(dim,plotStartingPoint_n,n_max,measuring_unit_x):
    x = list(range(plotStartingPoint_n,n_max+1))
    if(measuring_unit_x == "n"):
        return x
    if(measuring_unit_x == "mtx in Bytes"):
        for n in x:
            x[n-plotStartingPoint_n] = getNNZ(dim,n) * 8
        return x
    if(measuring_unit_x == "mtx+vec in Bytes"):
        for n in x:
            x[n-plotStartingPoint_n] = (getNNZ(dim,n) + pow(n,dim)) * 8
        return x
    if(measuring_unit_x == "mtx+2vec in Bytes"):
        for n in x:
            x[n-plotStartingPoint_n] = (getNNZ(dim,n) + 2*pow(n,dim)) * 8
        return x
    

# config
#-----------------------------------------------------------------------------------------------------------------------------

folder_string = "./results/400-4/"
data_type = "average" # "median" "max" "min"
plotStartingPoint_n = 8

# executor
plot_istl = True
plot_ref = True
plot_omp = False
plot_cuda = False

# different matrix formats (gko,mtx_data)
plot_csr = True
plot_ell = True
plot_coo = False

plot_cache_sizes = True
plot_RAM_size = True

# x-axis
# possible values: "n", "mtx+vec in Bytes" "mtx in Bytes"
measuring_unit_x = "mtx in Bytes"
# possible values: "no","nnz","N"
plot_per_devisor = "nnz" #"no"
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

# get file names (exclude folders and hidden files)
filenames = [file \
             for file in os.listdir(folder_string) \
             if os.path.isfile(folder_string+file) and not file.startswith('.')]
filenames.sort()

# file -> rawData
rawData = [getData(folder_string+file,data_type) for file in filenames]

# awDaxta -> plotData
x_3D = getXValues(3,plotStartingPoint_n,n_max,measuring_unit_x)
x_2D = getXValues(2,plotStartingPoint_n,n_max,measuring_unit_x)
devisors_2D = getDevisors(2,n_max,plot_per_devisor)
devisors_3D = getDevisors(3,n_max,plot_per_devisor)

plotData = [getPlotData(data,devisors_2D,devisors_3D,plotStartingPoint_n,n_max) for data in rawData]

print(x_3D)


# Add Data to Plots
figure, axis = plt.subplots(2, 2)
name = "no name assigned"
for file in range(0,len(filenames)):
    if(filenames[file][:4]=="ISTL"): 
        name = filenames[file]
        if(not plot_istl): continue
    if(filenames[file][:3]=="gko"): name = filenames[file][:15]
    if((not plot_ref) and name[8:11]=="ref"): continue
    if((not plot_omp) and name[8:11]=="omp"): continue
    if((not plot_cuda) and name[8:12]=="cuda"): continue
    if((not plot_csr) and (name[12:15]=="csr" or name[13:16]=="csr")): continue
    if((not plot_coo) and (name[12:15]=="coo" or name[13:16]=="coo")): continue
    if((not plot_ell) and (name[12:15]=="ell" or name[13:16]=="ell")): continue
    axis[0,0].plot(x_2D, plotData[file][0], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
    axis[1,0].plot(x_2D, plotData[file][1], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
    axis[0,1].plot(x_3D, plotData[file][2], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
    axis[1,1].plot(x_3D, plotData[file][3], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)

# Set titles
perDiv=""
if(plot_per_devisor=="nnz"): perDiv= " per NNZ"
if(plot_per_devisor=="N"): perDiv= " per N"
axis[0,0].set_title("d=2 average time to generate sparse matrix"+perDiv)
axis[1,0].set_title("d=2 average time to calculate SpMV"+perDiv)
axis[0,1].set_title("d=3 average time to generate sparse matrix"+perDiv)
axis[1,1].set_title("d=3 average time to calculate SpMV"+perDiv)



for ax in axis.flat:
    ax.set_xlabel(measuring_unit_x)
    ax.set_ylabel('time in nanoseconds')
    ax.legend()
    if(plot_y_log): ax.set_yscale('log')
    if(plot_x_log): ax.set_xscale('log')
    if(plot_cache_sizes):
        ax.axvline(x=L1_size_byte, color="grey", linestyle=':')
        ax.axvline(x=L2_size_byte, color="grey", linestyle='-.')
        ax.axvline(x=L3_size_byte, color="grey", linestyle='--')
    if(plot_RAM_size): ax.axvline(x=RAM_size_byte, color="grey", linestyle='-')

if(not plot_SpMV_d3_only):
    plt.show()
