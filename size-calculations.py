

#---------------------------------------------------------------------------
n_max = 2000 # bit-display works at least until n= 2 000 correctly with d=3
d = 3
#---------------------------------------------------------------------------

# csr size calculations
for n in range(1,n_max+1):
    N = 1
    for i in range(0,d):
        N *= n
    val_size_bits = 7*N*64
    val_size_MiB = val_size_bits/1024

    colInd_size_bits = val_size_bits
    colInd_size_MiB = val_size_MiB

    rowPtr_size_bits = N *64
    rowPtr_size_MiB = rowPtr_size_bits/1024

    mtx_size_bits = val_size_bits+colInd_size_bits+rowPtr_size_bits
    mtx_size_MiB= mtx_size_bits/1024

    # decide what to print here ---------------------------------------------
    display_string = 'matrix' #sum of all vectors

    if(display_string == 'matrix'):
        size_bits = mtx_size_bits
        size_MiB = mtx_size_MiB
    elif(display_string=="columnIndex"):
        size_bits = colInd_size_bits
        size_MiB = colInd_size_MiB
    #elif(display_string=="")

    #------------------------------------------------------------------------
    print("n="+str(n)+ display_string" size in bit: "+str(size_bits)+" in 1000MiB: "+str(mtx_size_MiB/1000))
    if(size_MiB>= 15109):
        print("! not fitting into NVIDIA Memory anymore!")
    