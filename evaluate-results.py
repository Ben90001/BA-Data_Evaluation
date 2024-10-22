import matplotlib.pyplot as plt
import os

# 1. Retrieve data from files & average them
# 2. transform data for each file in 4 plotable parts: 2D_Gen,2D_SpMV,3D_Gen,3D_SpMV
# 3. sort them into respective plots & decide which ones to plot

def getData(filename,rounds,n_max):
    # import data
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Split each line into integers and store them as a list
            row = list(map(int, line.split()))
            data.append(row)
    print(filename+": Data size: "+str(len(data)))
    return data
def getAverageData(filename,rounds,n_max):
    data = getData(filename,rounds,n_max)
    average_data = []
    for i in range(len(data)):
        if(i%rounds==0):
            sum_time_to_gen = 0
            sum_time_to_SpMV = 0
            j=1
            for j in range(0,rounds):
                sum_time_to_gen += data[i+j][3]
                sum_time_to_SpMV += data[i+j][4]
            average_time_to_gen = sum_time_to_gen/rounds
            average_time_to_SpMV = sum_time_to_SpMV/rounds
            average_data.append([data[i][0],data[i][1],average_time_to_gen,average_time_to_SpMV])
    print(filename+": Cleaned data size: "+ str(len(average_data)))
    print('\n')
    return average_data

def getNNZ(dim, n):
    if(dim==2):
        return 5*pow(n,dim) -2*n -2
    if(dim==3):
        return 7*pow(n,dim) -2*n*n -2*n -2
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
    if(measuring_unit_x == "mtx+vec in Bytes"):
        for n in x:
            x[n-plotStartingPoint_n] = (getNNZ(dim,n) + pow(n,dim)) * 8
        return x
    

# config
#-----------------------------------------------------------------------------------------------------------------------------

folder_string = "./results/400-4/"
# set to 1 to display all
plotStartingPoint_n = 15

# executor
plot_istl = True
plot_ref = True
plot_omp = False

# different matrix formats (gko,mtx_data)
plot_csr = True
plot_ell = False
plot_coo = False

# x-axis
# possible values: "n", "mtx+vec in Bytes"
measuring_unit_x = "mtx+vec in Bytes"
# possible values: "no","nnz","N"
plot_per_devisor = "nnz"
plot_y_log = False
plot_x_log = True
markersize = True

plot_cache_sizes = True
# Kib -> B
L1_size_byte = 32 * 1024 /8    # additional 32 for instructions
L2_size_byte = 512 * 1024 /8
L3_size_byte = 32768 * 1024 /8 # = 32MiB
RAM_size_byte = 534359343104    # free -b | grep Mem | awk '{print $7}'


plot_SpMV_d3_only = False
#-----------------------------------------------------------------------------------------------------------------------------

#extract n_upperBound and rounds
n_max, rounds = map(int, folder_string[len("./results/"):-1].split('-'))

# get file names (exclude folders and hidden files)
filenames = [file \
             for file in os.listdir(folder_string) \
             if os.path.isfile(folder_string+file) and not file.startswith('.')]
filenames.sort()

# file -> rawData
rawData = [getAverageData(folder_string+file,rounds,n_max) for file in filenames]

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
    if((not plot_csr) and name[12:15]=="csr"): continue
    if((not plot_coo) and name[12:15]=="coo"): continue
    if((not plot_ell) and name[12:15]=="ell"): continue

    axis[0,0].plot(x_2D, plotData[file][0], label=name, marker='s', markerfacecolor='none', markersize=markersize*3)
    axis[1,0].plot(x_2D, plotData[file][1], label=name, marker='s', markerfacecolor='none', markersize=markersize*3)
    axis[0,1].plot(x_3D, plotData[file][2], label=name, marker='s', markerfacecolor='none', markersize=markersize*3)
    axis[1,1].plot(x_3D, plotData[file][3], label=name, marker='s', markerfacecolor='none', markersize=markersize*3)

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
        ax.axvline(x=L1_size_byte, color="grey", linestyle='--')
        ax.axvline(x=L2_size_byte, color="grey", linestyle='--')
        ax.axvline(x=L3_size_byte, color="grey", linestyle='--')
        ax.axvline(x=RAM_size_byte, color="grey", linestyle='-')

if(not plot_SpMV_d3_only):
    plt.show()
