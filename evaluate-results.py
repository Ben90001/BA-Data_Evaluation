import matplotlib.pyplot as plt

# 1. Retrieve data from files
# 2. splitting data 4 parts: d2/d3 and generation/SpMV
# 3. sort them into respective plots(&lable&color)

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

# config
#-----------------------------------------------------------------------------------------------------------------------------
rounds = 5
n_max = 200

# different matrix formats (gko,ref,mtx_data)
plot_csr = True
plot_ell = True
# different assembly datastructure
plot_mtx_assembly_data = False
plot_mtx_assembly_data_setOnly = False
# parallel
plot_omp = False

plot_with_logarithmic_scale = True
plot_per_mtx_entry = True


plot_SpMV_d3_only = False
#-----------------------------------------------------------------------------------------------------------------------------

# note: assembly referes to "matrix_assemlby_data" vs. "matrix_data" classe used to assembly the matrix in ginkgo
folder_string = "./results/200-5/"
ISTL_data = getAverageData(folder_string+'results_ISTL.txt',rounds,n_max)
GINKGO_data_assembly = getAverageData(folder_string+'results_ginkgo_mtx-assembly-data__reference_csr.txt',rounds,n_max)
GINKGO_data_csr = getAverageData(folder_string+'results_ginkgo_mtx-data__reference_csr.txt',rounds,n_max)
GINKGO_data_ell = getAverageData(folder_string+'results_ginkgo_mtx-data_reference_ell.txt',rounds,n_max)
GINKGO_data_omp_csr = getAverageData(folder_string+'results_gko_mtx-data_omp_csr.txt',rounds,n_max)
GINKGO_data_assembly_setOnly = getAverageData(folder_string+'results_gko_mtx-assembly-data_ref_csr__set-value-only_diff-mtx-instantiation.txt',rounds,n_max)

# plain average plot data
x = list(range(1, n_max+1))

devisors_2D = getDevisors(2,n_max,plot_per_mtx_entry)
devisors_3D = getDevisors(3,n_max,plot_per_mtx_entry)

print(x)
d2_gen_istl = [ISTL_data[n-1][2]/devisors_2D[n] for n in x] 
d2_SpMV_istl = [ISTL_data[n-1][3]/devisors_2D[n] for n in x] 
d3_gen_istl = [ISTL_data[n_max+n-1][2]/devisors_3D[n] for n in x] 
d3_SpMV_istl = [ISTL_data[n_max+n-1][3]/devisors_3D[n] for n in x] 

d2_gen_ginkgo_asbly = [GINKGO_data_assembly[n-1][2]/devisors_2D[n] for n in x] 
d2_SpMV_ginkgo_asbly = [GINKGO_data_assembly[n-1][3]/devisors_2D[n] for n in x] 
d3_gen_ginkgo_asbly = [GINKGO_data_assembly[n_max+n-1][2]/devisors_3D[n] for n in x] 
d3_SpMV_ginkgo_asbly = [GINKGO_data_assembly[n_max+n-1][3]/devisors_3D[n] for n in x] 

d2_gen_ginkgo_csr = [GINKGO_data_csr[n-1][2]/devisors_2D[n] for n in x] 
d2_SpMV_ginkgo_csr = [GINKGO_data_csr[n-1][3]/devisors_2D[n] for n in x] 
d3_gen_ginkgo_csr = [GINKGO_data_csr[n_max+n-1][2]/devisors_3D[n] for n in x] 
d3_SpMV_ginkgo_csr = [GINKGO_data_csr[n_max+n-1][3]/devisors_3D[n] for n in x] 

d2_gen_ginkgo_ell = [GINKGO_data_ell[n-1][2]/devisors_2D[n] for n in x] 
d2_SpMV_ginkgo_ell = [GINKGO_data_ell[n-1][3]/devisors_2D[n] for n in x] 
d3_gen_ginkgo_ell = [GINKGO_data_ell[n_max+n-1][2]/devisors_3D[n] for n in x] 
d3_SpMV_ginkgo_ell = [GINKGO_data_ell[n_max+n-1][3]/devisors_3D[n] for n in x] 

d2_gen_ginkgo_omp = [GINKGO_data_omp_csr[n-1][2]/devisors_2D[n] for n in x] 
d2_SpMV_ginkgo_omp = [GINKGO_data_omp_csr[n-1][3]/devisors_2D[n] for n in x] 
d3_gen_ginkgo_omp = [GINKGO_data_omp_csr[n_max+n-1][2]/devisors_3D[n] for n in x] 
d3_SpMV_ginkgo_omp = [GINKGO_data_omp_csr[n_max+n-1][3]/devisors_3D[n] for n in x] 

d2_gen_ginkgo_asbly_sO = [GINKGO_data_assembly_setOnly[n-1][2]/devisors_2D[n] for n in x] 
d2_SpMV_ginkgo_asbly_sO = [GINKGO_data_assembly_setOnly[n-1][3]/devisors_2D[n] for n in x] 
d3_gen_ginkgo_asbly_sO = [GINKGO_data_assembly_setOnly[n_max+n-1][2]/devisors_3D[n] for n in x] 
d3_SpMV_ginkgo_asbly_sO = [GINKGO_data_assembly_setOnly[n_max+n-1][3]/devisors_3D[n] for n in x] 

# analysis plot data
#d3_SPMV_diff_ISTL_gko = [(GINKGO_data_assembly[n_max+n-1][3] - ISTL_data[n_max+n-1][3]) for n in x]

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



figure, axis = plt.subplots(2, 2)
# plain results
# ISTL
axis[0,0].plot(x, d2_gen_istl, color='blue', alpha=1, label='ISTL')
axis[1,0].plot(x, d2_SpMV_istl, color='blue', alpha=1, label='ISTL')
axis[0,1].plot(x, d3_gen_istl, color='blue', alpha=1, label='ISTL')
axis[1,1].plot(x, d3_SpMV_istl, color='blue', alpha=1, label='ISTL')
# gko mtx_assembly_data
if(plot_mtx_assembly_data):
    axis[0,0].plot(x, d2_gen_ginkgo_asbly, color='red', alpha=1, label='gko mtx_assembly_data')
    axis[1,0].plot(x, d2_SpMV_ginkgo_asbly, color='red', alpha=1, label='gko mtx_assembly_data')
    axis[0,1].plot(x, d3_gen_ginkgo_asbly, color='red', alpha=1, label='gko mtx_assembly_data')
    axis[1,1].plot(x, d3_SpMV_ginkgo_asbly, color='red', alpha=1, label='gko mtx_assembly_data')
# gko mtx-assembly-data using setValue only (no addValue)
if(plot_mtx_assembly_data_setOnly):
    axis[0,0].plot(x, d2_gen_ginkgo_asbly_sO, color='skyblue', alpha=1, label='gko mtx_assembly_data 2')
    axis[1,0].plot(x, d2_SpMV_ginkgo_asbly_sO, color='skyblue', alpha=1, label='gko mtx_assembly_data 2')
    axis[0,1].plot(x, d3_gen_ginkgo_asbly_sO, color='skyblue', alpha=1, label='gko mtx_assembly_data 2')
    axis[1,1].plot(x, d3_SpMV_ginkgo_asbly_sO, color='skyblue', alpha=1, label='gko mtx_assembly_data 2')
# gko Csr
if(plot_csr):
    axis[0,0].plot(x, d2_gen_ginkgo_csr, color='brown', alpha=1, label='gko Csr')
    axis[1,0].plot(x, d2_SpMV_ginkgo_csr, color='brown', alpha=1, label='gko Csr')
    axis[0,1].plot(x, d3_gen_ginkgo_csr, color='brown', alpha=1, label='gko Csr')
    axis[1,1].plot(x, d3_SpMV_ginkgo_csr, color='brown', alpha=1, label='gko Csr')
# gko Ell
if(plot_ell):
    axis[0,0].plot(x, d2_gen_ginkgo_ell, color='grey', alpha=1, label='gko Ell')
    axis[1,0].plot(x, d2_SpMV_ginkgo_ell, color='grey', alpha=1, label='gko Ell')
    axis[0,1].plot(x, d3_gen_ginkgo_ell, color='grey', alpha=1, label='gko Ell')
    axis[1,1].plot(x, d3_SpMV_ginkgo_ell, color='grey', alpha=1, label='gko Ell')
# gko omp
if(plot_omp):
    axis[0,0].plot(x, d2_gen_ginkgo_omp, color='purple', alpha=1, label='gko omp')
    axis[1,0].plot(x, d2_SpMV_ginkgo_omp, color='purple', alpha=1, label='gko omp')
    axis[0,1].plot(x, d3_gen_ginkgo_omp, color='purple', alpha=1, label='gko omp')
    axis[1,1].plot(x, d3_SpMV_ginkgo_omp, color='purple', alpha=1, label='gko omp')




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
