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


def getDevisors(dim, n_upperBound, plot_per_mtx_entry):
    if(not plot_per_mtx_entry):
        return [1]*(n_upperBound+1)
    devisors = list(range(0, n_upperBound+1))
    if(dim==2):
        for n in range(1, n_upperBound+1):
            devisors[n]= 5*pow(n,dim) -2*n -2
        return devisors
    elif(dim==3):
        for n in range(1, n_upperBound+1):
            devisors[n]= 7*pow(n,dim) -2*n*n -2*n -2
        return devisors
    raise ValueError(f"Invalid value for: {dim}")

#returns plotable arrays: 2D_Gen,2D_SpMV,3D_Gen,3D_SpMV
def getPlotData(data,devisors_2D,devisors_3D,plotStartingPoint_n,n_upperBound):
    plotData = [ \
        [data[n-1][2]/devisors_2D[n] for n in range(plotStartingPoint_n, n_upperBound+1)], \
        [data[n-1][3]/devisors_2D[n] for n in range(plotStartingPoint_n, n_upperBound+1)], \
        [data[n_upperBound+n-1][2]/devisors_3D[n] for n in range(plotStartingPoint_n, n_upperBound+1)], \
        [data[n_upperBound+n-1][3]/devisors_3D[n] for n in range(plotStartingPoint_n, n_upperBound+1)] \
    ]
    return plotData

# config
#-----------------------------------------------------------------------------------------------------------------------------

folder_string = "./results/400-4/"
# set to 1 to display all
plotStartingPoint_n = 20

# executor
plot_istl = True
plot_ref = True
plot_omp = False

# different matrix formats (gko,mtx_data)
plot_csr = True
plot_ell = False
plot_coo = False

# different assembly datastructure
#plot_gpu_mtx_data = True
#plot_gpu_mtx_data_setOnly = True

plot_with_logarithmic_scale = True
plot_per_mtx_entry = True


plot_SpMV_d3_only = False
#-----------------------------------------------------------------------------------------------------------------------------

#extract n_upperBound and rounds
n_max, rounds = map(int, folder_string[len("./results/"):-1].split('-'))

# get file names (exclude folders and hidden files)
filenames = [file \
             for file in os.listdir(folder_string) \
             if os.path.isfile(folder_string+file) and not file.startswith('.')]
filenames.sort()
print(filenames)

# file -> rawData
rawData = [getAverageData(folder_string+file,rounds,n_max) for file in filenames]

# rawData -> plotData
x = list(range(plotStartingPoint_n, n_max+1))
devisors_2D = getDevisors(2,n_max,plot_per_mtx_entry)
devisors_3D = getDevisors(3,n_max,plot_per_mtx_entry)
plotData = [getPlotData(data,devisors_2D,devisors_3D,plotStartingPoint_n,n_max) for data in rawData]

print(x)


# Add Data to Plots
figure, axis = plt.subplots(2, 2)
name = "no name assigned"
for file in range(0,len(filenames)):
    if(filenames[file][:4]=="ISTL"): name = filenames[file]
    if(filenames[file][:3]=="gko"): name = filenames[file][:15]
    if((not plot_ref) and name[8:11]=="ref"): continue
    if((not plot_omp) and name[8:11]=="omp"): continue
    if((not plot_csr) and name[12:15]=="csr"): continue
    if((not plot_coo) and name[12:15]=="coo"): continue
    if((not plot_ell) and name[12:15]=="ell"): continue

    axis[0,0].plot(x, plotData[file][0], label=name) #color='blue'
    axis[1,0].plot(x, plotData[file][1], label=name)
    axis[0,1].plot(x, plotData[file][2], label=name)
    axis[1,1].plot(x, plotData[file][3], label=name)

# Set titles
perNNZ=""
if(plot_per_mtx_entry): 
    perNNZ= " per NNZ"
axis[0,0].set_title("d=2 average time to generate sparse matrix"+perNNZ)
axis[1,0].set_title("d=2 average time to calculate SpMV"+perNNZ)
axis[0,1].set_title("d=3 average time to generate sparse matrix"+perNNZ)
axis[1,1].set_title("d=3 average time to calculate SpMV"+perNNZ)



for ax in axis.flat:
    ax.set_xlabel('n values')
    ax.set_ylabel('time in nanoseconds')
    ax.legend()
    if(plot_with_logarithmic_scale):
        ax.set_yscale('log')

if(not plot_SpMV_d3_only):
    plt.show()




# single plot
'''
if(plot_SpMV_d3_only):
    if(plot_csr): plt.plot(x, d3_SpMV_ginkgo_csr, label='Ginkgo')
    if(plot_mtx_assembly_data): plt.plot(x, d3_SpMV_ginkgo_asbly, label='Ginkgo assembly')
    plt.plot(x, d3_SpMV_istl, label='ISTL')
    #plt.plot(x, d3_SPMV_diff_ISTL_gko, label='Ginkgo(asbly)-ISTL', color='red')
    plt.xlabel('n values')
    plt.ylabel('time in nanoseconds')
    plt.title('d=3 SpMV: Average Times of '+str(rounds)+' rounds')
    plt.legend()
    if(plot_with_logarithmic_scale):
        plt.yscale('log')
    plt.show()
'''