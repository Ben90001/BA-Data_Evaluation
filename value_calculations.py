import numpy as np

peak_performance = 58.8 * 1000000000 #FLOPS/s
peak_sustainable_bandwidth = 49333333333 #B/s


def getNNZ(dim, n):
    if(dim==2):
        #old : return 5*pow(n,dim) -2*n -2
        return 5*n*n - 4*n
    if(dim==3):
        #old : return 7*pow(n,dim)
        return 7*n*n*n - 6*n*n
    raise ValueError(f"Invalid value for: {dim}")
def getN(dim,n):    
    return pow(n,dim)

# in FLOPS
def getWork(n,dim):
    return 2*getNNZ(dim,n)
# in Bytes
def getMemTrafic(n,dim):
    return (getNNZ(dim,n)+3*getN(dim,n)) *8 #read A, read x, read y, write y, in Bytes
    # assume x gets loaded only once (from RAM)
def getArithmeticIntnsity(n,dim):
    return getWork(n,dim)/getMemTrafic(n,dim)

#TODO: expansion for dim=2
def getRooflineValue(peak_performance, peak_sustainable_bandwidth, n, dim):
    return np.minimum(peak_performance, peak_sustainable_bandwidth * getArithmeticIntnsity(n,dim))