# BA-Data_Evaluation

### Data Format:
n dim round_id time_to_gen time_to_SpMV

### import data
1. copy the `BA-Ginkgo_vs_Dune/src/results/` folder into the `results` folder.
2. rename this folder in this fassion: n_max+"-"rounds_min  
    n_max being the maximum n in any of the data
    rounds_min being the minimum rounds any of the experiments (n-dim-combinations) have been generated.
3. move the log file into a directory, we dont want the code to try and plot it ;)

NOTE: `cpu`/`gpu` referes to the usage of `matrix_data`/ `matrix_assembly_data`. Host is determined by the executor: `ref`/`omp` for cpu, `cuda` for gpu.

