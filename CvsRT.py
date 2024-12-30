import pandas as pd
import sys
import os
import csv

def read_csv_to_dataframe(file_path):
    try:
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)

if __name__ == "__main__":

    # Check if file path is provided as command-line argument
    if sys.argv[1] == "help":
        print("Usage: python script.py <file_path> <output_file> <PARX> <timeOut>")
        sys.exit(1)
    #Get input data from user
    file_path_raw = input("Enter file path of raw.csv: ")
    output_file = input("Enter file path of output directory: ")
    input_cores = input("Enter number of cores (incrementing) used by the solvers, seperated by ' ':")
    slvrs_cores = list(map(int,input_cores.split(' ')))
    #DEBUG ========================================================
    print("slvrs_cores: " + slvrs_cores)
    #==============================================================

    dataframe = read_csv_to_dataframe(file_path_raw)
    # Group DataFrame by the "name" column
    grouped_df_solvers = dataframe.groupby("solver_name")
    
    # get array holding all names of the solvers
    names_solvers = grouped_df_solvers.groups.keys
    #DEBUG ========================================================
    print(names_solvers)
    #==============================================================
    #create array holding paths to the output files of a solver
    path_slvr_output = os.path.join(file_path_raw, names_solvers[0])
    #DEBUG ========================================================
    print(path_slvr_output)
    #==============================================================

    #iterate through instances
    csv_data = []
    for file_instance in os.listdir(path_slvr_output):
        filename_instance = os.fsdecode(file_instance)
        #DEBUG ========================================================
        print(filename_instance)
        #==============================================================
        # read nb_args after COI
        nb_args_after_coi = int(file_instance.readlines()[-1])
        #DEBUG ========================================================
        print("nb_args_after_coi: " + nb_args_after_coi)
        #==============================================================
        #check if args == 0, skip instances solves during preprocessing
        if nb_args_after_coi == 0:
            continue
        # for each instance compare RT for different solvers
        df_instances = grouped_df_solvers.loc[grouped_df_solvers['instance'] == filename_instance]
        #DEBUG ========================================================
        print(df_instances)
        #==============================================================
        # choose solver with minimum RT
        df_instances_min = df_instances[df_instances.runtime == df_instances.runtime.min()]
        #DEBUG ========================================================
        print(df_instances_min)
        sys.exit(1)
        #==============================================================
        # calculate nb_args/nb_cores
        nb_cores = slvrs_cores[names_solvers.index(df_instances_min.solver_name)]
        #DEBUG ========================================================
        print("nb_cores: " + nb_cores)
        #==============================================================
        # save in csv_data: instance_name, nb_args_after_coi, nb_cores
        if not csv_data:
            csv_data = [{'solver_name': df_instances_min.solver_name, 'nb_args_after_coi' : nb_args_after_coi, 'nb_cores' : nb_cores}]
        else:
            csv_data.append({'solver_name': df_instances_min.solver_name, 'nb_args_after_coi' : nb_args_after_coi, 'nb_cores' : nb_cores})
        #DEBUG ========================================================
        print("csv_data: " + csv_data)
        sys.exit(1)
        #==============================================================
    
    #write csv file
    with open('analysis_CvsRT.csv', 'w', newline='') as csvfile:
        fieldnames = ['solver_name', 'nb_args_after_coi', 'nb_cores']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)       
    