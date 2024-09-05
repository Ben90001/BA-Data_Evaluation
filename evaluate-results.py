import matplotlib.pyplot as plt


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

rounds = 5
n_max = 200
ISTL_data = getAverageData('results_ISTL.txt',rounds,n_max)
GINKGO_data = getAverageData('results_ginkgo_reference_csr.txt',rounds,n_max)

# plot average values
x = list(range(1, n_max+1))
print(x)
d2_gen_istl = [ISTL_data[value-1][2] for value in x] 
d2_SpMV_istl = [ISTL_data[value-1][3] for value in x] 
d3_gen_istl = [ISTL_data[n_max+value-1][2] for value in x] 
d3_SpMV_istl = [ISTL_data[n_max+value-1][3] for value in x] 

d2_gen_ginkgo = [GINKGO_data[value-1][2] for value in x] 
d2_SpMV_ginkgo = [GINKGO_data[value-1][3] for value in x] 
d3_gen_ginkgo = [GINKGO_data[n_max+value-1][2] for value in x] 
d3_SpMV_ginkgo = [GINKGO_data[n_max+value-1][3] for value in x] 



figure, axis = plt.subplots(2, 2)

axis[0,0].plot(x, d2_gen_istl, color='blue', alpha=1, label='ISTL')
axis[0,0].plot(x, d2_gen_ginkgo, color='green', alpha=1, label='Ginkgo')#, linestyle='None', marker='x')
axis[0, 0].set_title("d=2 average time to generate sparse matrix")

axis[1,0].plot(x, d2_SpMV_istl, color='blue', alpha=1, label='ISTL')
axis[1,0].plot(x, d2_SpMV_ginkgo, color='green', alpha=1, label='Ginkgo')
axis[1, 0].set_title("d=2 average time to calculate SpMV")

axis[0,1].plot(x, d3_gen_istl, color='blue', alpha=1, label='ISTL')
axis[0,1].plot(x, d3_gen_ginkgo, color='green', alpha=1, label='Ginkgo')
axis[0, 1].set_title("d=3 average time to generate sparse matrix")

axis[1,1].plot(x, d3_SpMV_istl, color='blue', alpha=1, label='ISTL')
axis[1,1].plot(x, d3_SpMV_ginkgo, color='green', alpha=1, label='Ginkgo')
axis[1, 1].set_title("d=3 average time to calculate SpMV")



for ax in axis.flat:
    ax.set_xlabel('n values')
    ax.set_ylabel('time in nanoseconds')
    ax.legend()
    #ax.set_yscale('log')


#plt.yscale('log')
#plt.xlabel('n values')
#plt.ylabel('time in nanoseconds')
#plt.title('Average Times of '+str(rounds)+' rounds')
#plt.legend()  # Show the legend

plt.show()
