def sizeCalculation_bit(n,d,x,y,data_string):
    if(data_string=="xN"):
        N = 1
        for i in range(0,d):
            N *= n
        return (x*N)*64
    if(data_string=="xN+y"):
        N = 1
        for i in range(0,d):
            N *= n
        return (x*N+y)*64
    if(data_string=="Mtx+Vec"):
        N = pow(n,d)
        if(d==3): return (7*N -2*n*n -2*n -2)*64
        if(d==2): return (5*N -2*n -2)*64
    if(data_string=="xn^2+yn+z"): #part of x vector needed per yi calc (+row of A)
        return (x*n*n+y*n+z)*64
    
    raise ValueError("sizeCalculation: data_string unknown")
    



KiB_bitSize = 1024
MiB_bitSize = 1048576
GiB_bitSize = 1073741824

#----------------------------------------------------------------------------------------------
n_lowerBound = 1
n_upperBound = 4000 # bit-scale works at least until n=2000 correctly with d=3 
d = 3

# this can be: "xN","xN+y","Mtx+Vec", "xn^2+yn+z"
data_string = "Mtx+Vec"    # number of elemets with each 64bit 
x=2
y=0
z=(2*d+1)
#y=(2*d+1)*3

# values to exceed 
    # L1 and L2 distributed across 64 cores 
    # according to lscpu
    #L1_size_bit = (4 * MiB_bitSize) / 64
    #L2_size_bit = (64 * MiB_bitSize) /64
    #L3_size_bit = 512 * MiB_bitSize
# according to cat /sys/devices/system/cpu/cpu*/cache/index*/size
L1_size_bit = 32 * KiB_bitSize    # additional 32 for instructions
L2_size_bit = 512 * KiB_bitSize
L3_size_bit = 32768 * KiB_bitSize # = 32MiB

RAM_size_bit = 503 * GiB_bitSize
#----------------------------------------------------------------------------------------------
L1_exceeded = False
L2_exceeded = False
L3_exceeded = False
RAM_exceeded = False
for n in range(n_lowerBound,n_upperBound+1):
    dataSize = sizeCalculation_bit(n,d,x,y,data_string)/8
    #print(str(dataSize))
    if((dataSize>L1_size_bit) and not L1_exceeded):
        L1_exceeded = True
        print(data_string+"("+f"{dataSize/MiB_bitSize:.2f}"+"MiB) exceeds L1 at: n="+str(n)+" d="+str(d))
    if((dataSize>L2_size_bit) and not L2_exceeded):
        L2_exceeded = True
        print(data_string+"("+f"{dataSize/MiB_bitSize:.2f}"+"MiB) exceeds L2 at: n="+str(n)+" d="+str(d))
    if((dataSize>L3_size_bit) and not L3_exceeded):
        L3_exceeded = True
        print(data_string+"("+f"{dataSize/MiB_bitSize:.2f}"+"MiB) exceeds L3 at: n="+str(n)+" d="+str(d))
    if((dataSize>RAM_size_bit) and not RAM_exceeded):
        RAM_exceeded = True
        print(data_string+"("+f"{dataSize/GiB_bitSize:.2f}"+"GiB) exceeds RAM at: n="+str(n)+" d="+str(d))
print("----finished----")
