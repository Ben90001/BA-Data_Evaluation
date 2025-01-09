import filecmp
import numpy as np
import scipy

from value_calculations import *
from evaluate_results import *

def getFilenames(folder_string):
    filenames = [file \
            for file in os.listdir(folder_string) \
            if os.path.isfile(folder_string+file) and not file.startswith('.')]
    return filenames#.sort()

def getGroupedFiles(filenames):
    # Grouping filenames
    groups = defaultdict(list)
    for filename in filenames:
        # Extract the first value pair (before '_')
        key = '_'.join(filename.split('_')[:2])
        groups[key].append(filename)

    # Convert to a regular dictionary (optional)
    grouped_files = dict(groups)

    # Print grouped files
    #for key, group in grouped_files.items():
        #print(f"Group {key}: {group}")
    return grouped_files

def read_mtx_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Ignore comments and metadata lines
    data_lines = [line.strip() for line in lines if not line.startswith('%')]
    size_line = data_lines[0]  # The first non-comment line contains the dimensions
    
    # Handle potential sparse matrix format
    if len(data_lines) > 1 and len(data_lines[1].split()) > 1:
        # If subsequent lines have more than one value, interpret as sparse format
        data = [float(line.split()[-1]) for line in data_lines[1:]]
    else:
        # Otherwise, assume dense format
        data = [float(value) for value in data_lines[1:]]
    
    return size_line, np.array(data)

def compare_mtx_files(file1,file2):
        matrix1 = scipy.io.mmread(file1)
        matrix2 = scipy.io.mmread(file2)
        # Check if both matrices have the same shape
        if matrix1.shape != matrix2.shape:
            return False, "Matrices have different shapes"

        if scipy.sparse.issparse(matrix1) and scipy.sparse.issparse(matrix2):
            return (matrix1 != matrix2).nnz == 0, "Matrices are identical"  # Check if non-zero entries are the same
        else:
            return compare_mtx_files_dense(file1,file2)

        

def compare_mtx_files_dense(file1, file2, tol=1e-6):
    size1, data1 = read_mtx_file(file1)
    size2, data2 = read_mtx_file(file2)
    
    if size1 != size2:
        return False, f"Size mismatch: {size1} vs {size2}"
    
    if not np.allclose(data1, data2, atol=tol):
        return False, "Data mismatch within tolerance."
    
    #*if not np.allclose(data1, data2, atol=tol):
        mismatches = np.where(~np.isclose(data1, data2, atol=tol))[0]
        mismatch_details = [
            f"Index {idx}: File1={data1[idx]}, File2={data2[idx]}"
            for idx in mismatches
        ]
        return False, f"Data mismatch:\n" + "\n".join(mismatch_details)
    
    return True, "Files match."

def verifyGroupedFiles(grouped_files,folder_string):
    # initialize values to return
    passing_count_ISTL_group = 0
    passing_count_GKO_group = 0
    passing_count_between_groups = 0

    ISTL_group_comparisons = 0
    GKO_group_comparisons = 0
    between_groups_comparisons = 0

    # make comparisons
    for n in range(1,max_verify+1):
        #Only dim=3 !!
        for dim in range(3,3+1):
            baseISTL = ""
            baseGKO = ""
            for filename in sorted(grouped_files[str(n)+"_"+str(dim)],reverse=True):
                components = filename.split('_')
                shift=0
                if components[2]=="x": shift = 2 # adjust as x_y is split into two components
                # compare within ISTL
                if components[3+shift] == "ISTL":
                    if baseISTL == "":
                        baseISTL = filename
                    elif compare_ISTL_group:
                        ISTL_group_comparisons+=1
                        if filecmp.cmp(folder_string+baseISTL, folder_string+filename, shallow=False):
                            passing_count_ISTL_group +=1
                            if print_matching: print("ISTL: "+baseISTL+" and "+filename+" are identical.")
                        else:
                            if print_non_matching: print("ISTL: "+baseISTL+" and "+filename+" are NOT identical!")
                # compare within Ginkgo
                elif components[3+shift] == "gko":
                    if baseGKO == "":
                        baseGKO = filename
                    elif compare_GKO_group:
                        GKO_group_comparisons+=1
                        if filecmp.cmp(folder_string+baseGKO, folder_string+filename, shallow=False):
                            passing_count_GKO_group+=1
                            if print_matching: print("GKO: "+baseGKO+" and "+filename+" are identical.")
                        else:
                            if print_non_matching: print("GKO: "+baseGKO+" and "+filename+" are NOT identical!")
            # compare the Groups
            if((not baseISTL=="") and (not baseGKO=="") and compare_between_groups):
                between_groups_comparisons+=1
                isSame, message = compare_mtx_files(folder_string+baseISTL,folder_string+baseGKO)
                if isSame:
                    passing_count_between_groups+=1
                    if print_matching: print(baseGKO+" and "+baseISTL+" are identical.")
                else:
                    if print_non_matching: print(baseGKO+" and "+baseISTL+" are NOT identical!"+message)
    if(folder_string[-2:-1]=="A"):
        print()
        print("baseISTL:"+baseISTL)
        print("baseGKOL:"+baseGKO)
        print()
    return [passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups, \
             ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons]


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
max_verify = 30
#Only dim=3 !!

verify_A = False
verify_y = True
verify_x_k_jac = True
verify_x_k_ilu = True

print_non_matching = True
print_matching = False

compare_ISTL_group = True
compare_GKO_group = True
compare_between_groups = True
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


folder_string = folder_string+"result-verification/"
filenames_A = getFilenames(folder_string+"A/")
filenames_y = getFilenames(folder_string+"y/")
filenames_x_k_jac = getFilenames(folder_string+"x_k_jac/")
filenames_x_k_ilu = getFilenames(folder_string+"x_k_ilu/")

if(verify_A):
    passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups,\
        ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons = \
        verifyGroupedFiles(getGroupedFiles(filenames_A),folder_string+"A/")
    print("Verifying A")
    print("ISTL Group passing: "+str(passing_count_ISTL_group)+"/"+str(ISTL_group_comparisons))
    print("GKO Group passing: "+str(passing_count_GKO_group)+"/"+str(GKO_group_comparisons))
    print("Between Groups passing: "+str(passing_count_between_groups)+"/"+str(between_groups_comparisons))
if(verify_y):
    print("Verifying y")
    passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups,\
        ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons = \
        verifyGroupedFiles(getGroupedFiles(filenames_y),folder_string+"y/")
    print("ISTL Group passing: "+str(passing_count_ISTL_group)+"/"+str(ISTL_group_comparisons))
    print("GKO Group passing: "+str(passing_count_GKO_group)+"/"+str(GKO_group_comparisons))
    print("Between Groups passing: "+str(passing_count_between_groups)+"/"+str(between_groups_comparisons))
if(verify_x_k_jac):
    print("Verifying x_k_jac")
    passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups,\
        ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons = \
        verifyGroupedFiles(getGroupedFiles(filenames_x_k_jac),folder_string+"x_k_jac/")
    print("ISTL Group passing: "+str(passing_count_ISTL_group)+"/"+str(ISTL_group_comparisons))
    print("GKO Group passing: "+str(passing_count_GKO_group)+"/"+str(GKO_group_comparisons))
    print("Between Groups passing: "+str(passing_count_between_groups)+"/"+str(between_groups_comparisons))
if(verify_x_k_ilu):
    print("Verifying x_k_ilu")
    passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups,\
        ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons = \
        verifyGroupedFiles(getGroupedFiles(filenames_x_k_ilu),folder_string+"x_k_ilu/")
    print("ISTL Group passing: "+str(passing_count_ISTL_group)+"/"+str(ISTL_group_comparisons))
    print("GKO Group passing: "+str(passing_count_GKO_group)+"/"+str(GKO_group_comparisons))
    print("Between Groups passing: "+str(passing_count_between_groups)+"/"+str(between_groups_comparisons))



                    