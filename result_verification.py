import filecmp
import numpy as np

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

def compare_mtx_files(file1, file2, tol=1e-6):
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
        for dim in range(2,3+1):
            baseISTL = ""
            baseGKO = ""
            for filename in sorted(grouped_files[str(n)+"_"+str(dim)],reverse=True):
                components = filename.split('_')
                shiftOnce=False
                if components[2]=="x": shiftOnce = True # adjust as x_y is split into two components
                # compare within ISTL
                if components[3+shiftOnce] == "ISTL":
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
                elif components[3+shiftOnce] == "gko":
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
    return [passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups, \
             ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons]


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
max_verify = 50

verify_A = True
verify_y = True
verify_x_k = True

print_non_matching = False
print_matching = False

compare_ISTL_group = False
compare_GKO_group = True
compare_between_groups = True
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


folder_string = folder_string+"result-verification/"
filenames_A = getFilenames(folder_string+"A/")
filenames_y = getFilenames(folder_string+"y/")
filenames_x_k = getFilenames(folder_string+"x_k/")

if(verify_A):
    print("Verifying A")
    passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups,\
        ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons = \
        verifyGroupedFiles(getGroupedFiles(filenames_A),folder_string+"A/")
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
if(verify_x_k):
    print("Verifying x_k")
    passing_count_ISTL_group, passing_count_GKO_group, passing_count_between_groups,\
        ISTL_group_comparisons,GKO_group_comparisons,between_groups_comparisons = \
        verifyGroupedFiles(getGroupedFiles(filenames_x_k),folder_string+"x_k/")
    print("ISTL Group passing: "+str(passing_count_ISTL_group)+"/"+str(ISTL_group_comparisons))
    print("GKO Group passing: "+str(passing_count_GKO_group)+"/"+str(GKO_group_comparisons))
    print("Between Groups passing: "+str(passing_count_between_groups)+"/"+str(between_groups_comparisons))




                    