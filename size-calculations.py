def sizeCalculation(n,d,x,y,data_string):
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
    
    raise ValueError("sizeCalculation: data_string unknown")
    



KiB_bitSize = 1024
MiB_bitSize = 1048576
GiB_bitSize = 1073741824

#---------------------------------------------------------------------------
n_lowerBound = 1
n_upperBound = 2000 # bit-scale works at least until n= 2 000 correctly with d=3
d = 3

# this can be: "xN","xN+y" 
data_string = "xN+y"    # number of elemets with each 64bit
x=1
y=(2*d+1)*3

# values to exceed
L1_size_bit = (4 * MiB_bitSize) / 64
L2_size_bit = (64 * MiB_bitSize) /64
L3_size_bit = 512 * MiB_bitSize
RAM_size_bit = 503 * GiB_bitSize
#---------------------------------------------------------------------------

L1_exceeded = False
L2_exceeded = False
L3_exceeded = False
for n in range(n_lowerBound,n_upperBound+1):
    dataSize = sizeCalculation(n,d,x,y,data_string)
    #print(str(dataSize))
    if((dataSize>L1_size_bit) and not L1_exceeded):
        L1_exceeded = True
        print(data_string+" exceeds L1 at: n="+str(n)+" d="+str(d))
    if((dataSize>L2_size_bit) and not L2_exceeded):
        L2_exceeded = True
        print(data_string+" exceeds L2 at: n="+str(n)+" d="+str(d))
    if((dataSize>L3_size_bit) and not L3_exceeded):
        L3_exceeded = True
        print(data_string+" exceeds L3 at: n="+str(n)+" d="+str(d))
print("----finished----")
