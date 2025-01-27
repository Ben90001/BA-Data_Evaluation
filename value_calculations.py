import numpy as np

peak_performance = 58.8 * 1000000000 #FLOPS/s
peak_sustainable_bandwidth = 49333333333 #B/s


def getN(dim,n):    
    return pow(n,dim)
def getNNZ(dim, n):
    if(dim==2):
        #old : return 5*pow(n,dim) -2*n -2
        return 5*n*n - 4*n
    if(dim==3):
        #old : return 7*pow(n,dim)
        return 7*n*n*n - 6*n*n
    raise ValueError(f"Invalid value for: {dim}")
# in elements
def getMatrixSize(dim,n,format):
    if(format == "optimal"):
        return getNNZ(dim,n)
    elif(format == "csr"):
        return (getNNZ(dim,n)+getNNZ(dim,n)+getN(dim,n)) # value_array, columnPtr_array, rowPtr_array

# in FLOPS
def getWork(n,dim):
    return 2*getNNZ(dim,n)
# in Bytes
def getMemTrafic(n,dim,mtx_format):
    return (getMatrixSize(dim,n,mtx_format)+3*getN(dim,n)) *8 #read A, read x, read y, write y, in Bytes
    # assume x gets loaded only once (from RAM)
def getArithmeticIntnsity(n,dim,mtx_format):
    return getWork(n,dim)/getMemTrafic(n,dim,mtx_format)

def getRooflineValue(peak_performance, peak_sustainable_bandwidth, n, dim, mtx_format):
    return np.minimum(peak_performance, peak_sustainable_bandwidth * getArithmeticIntnsity(n,dim,mtx_format))



#print("nnz verification: ")
#print("d=2, n = 100, nnz= "+str(getNNZ(2,100))) # should be 49 600
#print("d=3, n = 100, nnz= "+str(getNNZ(3,100))) # should be 6 940 000
#print("d=2, n = 101, nnz= "+str(getNNZ(2,101))) # should be 50 601
#print("d=3, n = 101, nnz= "+str(getNNZ(3,101))) # should be 7 150 901
