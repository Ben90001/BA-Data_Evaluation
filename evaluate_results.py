import matplotlib.pyplot as plt
import os
import statistics
from collections import defaultdict
import sys
import pickle

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
# rawData[n](n,dim,reps,time) -> [dataType][n](averageTime)
def getData(folder_string, dataDirectoryName, dataTypes):
    averagedDatas = [[],[],[],[]]

    for i in range(0,len(dataTypes)):
        data= getRawData(folder_string+"data/"+dataDirectoryName+"/"+dataTypes[i]+".txt")
        averagedData = [row[3]/row[2] for row in data] #calculating time average per rep
        for j in range(0,plotStartingPoint_n-1):
            averagedData[j] = np.nan
        averagedDatas[i]= averagedData
    return averagedDatas

    ''''
    memoization_folder = folder_string+"processedData/"
    filename = dataDirectoryName+".pkl"
    if os.path.exists(memoization_folder+filename):
        with open(memoization_folder+filename, "rb") as file:
            return pickle.load(file)
    os.makedirs(memoization_folder, exist_ok=True)
    
    i=0
    #[dataType][n](n,dim,time)
    processedValues = [[],[],[],[]]
    for dataType in dataTypes:
        data = getRawData(folder_string+"data/"+dataDirectoryName+"/"+dataType+".txt")
        #(n,dim) -> tuple-list of values
        map = defaultdict(list)
        # dim unnecessary with new data format
        for n, dim, rep, time  in data: map[(n,dim)].append((time))


        for (n, dim), values in map.items():
            processedValue = []
            if(processing_type == "average"):
                processedValue = [n,dim, statistics.mean(values)]
            elif(processing_type == "median"):
                processedValue = [n,dim, statistics.median(values)]
            elif(processing_type == "max"):
                processedValue = [n,dim, max(values)]
            elif(processing_type == "min"):
                processedValue = [n,dim, min(values)]
            else:
                raise ValueError("processing_type not not known")
            
            processedValues[i].append(processedValue)

        processedValues[i].sort(key=lambda x: x[0])
        print(dataType+": "+dataDirectoryName+": Processed data size: "+ str(len(processedValues[i])))
        i+=1
    if debug_mode: print("Debug: Finished \"Dataset\"")

    # append all other timings to the gen timings array
    #print("before returning: processedValues"+str(processedValues))
    for i in range(0,len(processedValues[0])):
        processedValues[0][i].append(processedValues[1][i][2]) #SpMV
        processedValues[0][i].append(processedValues[2][i][2]) #CG_jac
        processedValues[0][i].append(processedValues[3][i][2]) #CG_ilu
    #print("returning processedValues[0]"+str(processedValues[0]))
    
    # memoize for future
    with open(memoization_folder+filename, "wb") as file:
        pickle.dump(processedValues[0], file)

    return processedValues[0]
    '''

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

# input data:
#   data [0][n] = gen_time_averaged
#   data [1][n] = SpMV_time_averaged
#   data [2][n] = CGjac_time_averaged
#   data [3][n] = CGilu_time_averaged
# returns plotable y-values: Gen,SpMV,CG_jac,CG_ilu
def getPlotData(data,devisors,plotStartingPoint_n,n_max,dim,plot_performance):
    if plot_performance:
        # transform time->performance
        for i in range(0,len(data)):
            for n_minusOne in range(0,len(data[0])):
                # work in GFLOPs / time in s
                data[i][n_minusOne] = (getWork(n_minusOne+1,dim)/1000000000) / (data[i][n_minusOne]/1000000000) 


    gen_data = [data[0][n_minusOne]/devisors[n_minusOne+1] for n_minusOne in range(0,len(data[0]))]
    SpMV_data = [data[1][n_minusOne]/devisors[n_minusOne+1] for n_minusOne in range(0,len(data[1]))]
    CGjac_data = [data[2][n_minusOne]/devisors[n_minusOne+1] for n_minusOne in range(0,len(data[2]))]
    CGilu_data = [data[3][n_minusOne]/devisors[n_minusOne+1] for n_minusOne in range(0,len(data[3]))]
    ''''
    #index of next datapoint
    i=0 
    # skip all entries with n below plotStartingPoint_n from adding into PlotData
    while(data[i][0]< plotStartingPoint_n and i+1<len(data)): i+=1

    # build Array of PlotData
    for n in range(1,n_max+1):
        if data[i][0] == n:
            gen_data.append(data[i][2]/devisors[n])
            SpMV_data.append(data[i][3]/devisors[n])
            CGjac_data.append(data[i][4]/devisors[n])
            CGilu_data.append(data[i][5]/devisors[n])
            if(i+1<len(data)): i+=1
        else: # no values for skipped n
            gen_data.append(None)
            SpMV_data.append(None)
            CGjac_data.append(None)
            CGilu_data.append(None)
    '''
    plotData = [gen_data,SpMV_data,CGjac_data,CGilu_data]
    return plotData

def getRooflinePlot(dim, n_values,devisors,plotStartingPoint_n,mtx_format):
    result = []
    for n in n_values:
        value = None
        if n >= plotStartingPoint_n:
            # *1Mrd summ over nanosecs, 
            value = 1000000000*(getWork(n,dim)/(getRooflineValue(peak_performance,peak_sustainable_bandwidth, n, dim,mtx_format)))/ devisors[n] #unter erstem Bruch 1000000000*
            if plot_performance:
                value = getWork(n,dim)/value # devide by 1 billion cancels out (work: flops -> Gflops, time ns->s)
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

#folder_string = "./results/80-2-10-3d/"
folder_string = "./results/210-7-10-3d/"
plotStartingPoint_n = 12
# get info from foldername
n_max, min_reps, max_iters, dim = map(int, folder_string[len("./results/"):-1].replace("d", "").split('-'))
#n_max=400 #for smaller plot range overwrite n_max

plot_performance = False
plot_roofline = True

plot_istl = True
plot_gko = True
# used for getMatrixSize
mtx_format = "csr"


# executor
plot_ref = True
plot_1omp = True
plot_omp = True
plot_cuda = False

# assembly data structure
plot_md = True
plot_mad = False


# different matrix formats (gko,mtx_data)
plot_csr = True
plot_ell = True
plot_coo = True
plot_sellp = True

# ISTL BuildModes
plot_implicit = True
plot_row_wise = True
plot_random = True

# special data
plot_No2 = True
plot_minor_deviations = True

plot_cache_sizes = True
plot_L1 = True
plot_L2 = True
plot_L3 = True
plot_RAM_size = False

# x-axis
# possible values: "n", "mtx+vec in Bytes" "mtx in Bytes"
measuring_unit_x = "mtx in Bytes"
# y-axis 
# possible values: "no","nnz","N" missing: "byte" -> divisor=mtx size
plot_per_devisor = "nnz"

plot_y_log = False
plot_x_log = True
plot_sharedxy = False
plot_marker = False


plot_SpMV_only = False
debug_mode = False
#-----------------------------------------------------------------------------------------------------------------------------

# Kib -> B
L1_size_byte = 32 * 1024     # additional 32 for instructions
L2_size_byte = 512 * 1024 
L3_size_byte = 32768 * 1024  # = 32MiB
RAM_size_byte = 534359343104   # free -b | grep Mem | awk '{print $7}'
# each_numa =  264 GB          # cat /sys/devices/system/node/node*/meminfo

if plot_performance:
    plot_SpMV_only = True
    plot_per_devisor="no"

# if called from roofline file
if (not __name__ == "__main__"):
    plot_per_devisor = "no"
    print("Devisors deactivated for roofline diagram")



dataTypes = ["gen", "SpMV", "CGjac","CGilu"]

# get file names 
# (exclude folders and hidden files) 
# (remove first file component)
dataDirectoryNames = [folder \
            for folder in os.listdir(folder_string+"/data/") \
            if os.path.isdir(folder_string+"/data/"+folder) and not folder.startswith('.')]
dataDirectoryNames.sort()
if debug_mode: print("dataDirectoryNames: \n"+str(dataDirectoryNames))

# file -> processedData
processedDatas= [getData(folder_string, dataDirectoryName, dataTypes) for dataDirectoryName in dataDirectoryNames]
if debug_mode: print("processedDatas \n"+ str(processedDatas))
#rawDatas2D = []#[file[0] for file in rawDatas]
#rawDatas3D = processedDatas
#rawDatas3D = [file[1] for file in rawDatas]

# processedData -> plotData
n_values = list(range(1, n_max+1))
if debug_mode: print("n_values \n"+ str(n_values))
x_values = getXValues(dim,n_values,measuring_unit_x)
devisors = getDevisors(dim,n_max,plot_per_devisor)
if debug_mode: print("devisors \n"+ str(devisors))

# [file][dataType][n]
plotData = [getPlotData(data,devisors,plotStartingPoint_n,n_max,dim,plot_performance) for data in processedDatas]
if debug_mode: print("plotData[0] \n"+ str(plotData[0]))
rooflineValues= getRooflinePlot(dim,n_values,devisors,plotStartingPoint_n,mtx_format)

if __name__ == "__main__":
    # Add Data to Plots
    if plot_sharedxy: 
        figure, axis = plt.subplots(4, 1, sharex=True, sharey=True)
    else:
        figure, axis = plt.subplots(4, 1)
    name = "no name assigned"
    
    for file in range(0,len(dataDirectoryNames)):
        isGKO=False
        name = dataDirectoryNames[file][:-4]
        filename_components = name.split('_')
        if(filename_components[0]=="ISTL"):
            if not plot_istl: continue
            if (not plot_implicit and filename_components[1]=="implicit"): continue
            if (not plot_row_wise and filename_components[1]=="row"): continue
            if (not plot_random and filename_components[1]=="random"): continue

        if(filename_components[0] == "gko"): 
            isGKO = True
            if not plot_gko: continue
            if((not plot_md) and filename_components[1] == "md"): continue
            if((not plot_mad) and filename_components[1] == "mad"): continue
            if((not plot_ref) and filename_components[2] == "ref"): continue 
            if((not plot_1omp) and filename_components[2] == "1omp"): continue 
            if((not plot_omp) and filename_components[2] == "omp"): continue 
            if((not plot_cuda) and filename_components[2] == "cuda"): continue
            if((not plot_csr) and filename_components[3] == "csr"): continue  
            if((not plot_coo) and filename_components[3] == "coo"): continue 
            if((not plot_ell) and filename_components[3] == "ell"): continue  
            if((not plot_sellp) and filename_components[3] == "sellp"): continue  
            del filename_components[4:7]
        if(not plot_No2 and filename_components[-1]== "No2"): continue
        if(not plot_minor_deviations and filename_components[-1]!= "No2" and 4<len(filename_components)+isGKO): continue

        name = '_'.join(filename_components)

        axis[0].plot(x_values, plotData[file][0], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
        axis[1].plot(x_values, plotData[file][1], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
        axis[2].plot(x_values, plotData[file][2], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
        axis[3].plot(x_values, plotData[file][3], label=name, marker='s', markerfacecolor='none', markersize=plot_marker*3)
    if plot_roofline:
        axis[1].plot(x_values, rooflineValues, label="roofline", color="black")

    # Set titles
    perDiv=""
    if(plot_per_devisor=="nnz"): perDiv= " per NNZ"
    if(plot_per_devisor=="N"): perDiv= " per N"
    if plot_performance:
        axis[1].set_title("average Performance calculating SpMV (dim=3)"+perDiv)
    else:
        axis[0].set_title("d=3 average time to generate sparse matrix"+perDiv)
        axis[1].set_title("d=3 average time to calculate SpMV"+perDiv)
        axis[2].set_title("d=3 average time to run CG_jac with "+str(max_iters)+"Iterations"+perDiv)
        axis[3].set_title("d=3 average time to run CG_ilu with "+str(max_iters)+"Iterations"+perDiv)
    


    for ax in axis.flat:
        ax.set_xlabel(measuring_unit_x)
        if plot_performance:
            ax.set_ylabel('GFLOPS/s')
        else:
            ax.set_ylabel('time in nanoseconds')
        if(plot_y_log): ax.set_yscale('log')
        if(plot_x_log): ax.set_xscale('log')
        if(plot_cache_sizes):
            if plot_L1:
                ax.axvline(x=L1_size_byte, color="grey", linestyle=':', label="L1 Cache")
            if plot_L2:
                ax.axvline(x=L2_size_byte, color="grey", linestyle='-.',label="L2 Cache")
            if plot_L3:
                ax.axvline(x=L3_size_byte, color="grey", linestyle='--', label="L3 Cache")
        if(plot_RAM_size): ax.axvline(x=RAM_size_byte, color="grey", linestyle='-')
        if(plot_y_log): ax.set_ylim(bottom=1) 
        else: ax.set_ylim(bottom=0)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(top=0.95, bottom=0.05, hspace=0.5)
    # Move the plot to the left
    plt.subplots_adjust(right=0.7)

    if plot_SpMV_only:
        for i,ax in enumerate(axis):
            if not i==1:
                ax.set_visible(False)

        plt.subplots_adjust(top=1.1, bottom=-0.25, hspace=-0.8, left=0.05, right=0.81)

    plt.show()
    
