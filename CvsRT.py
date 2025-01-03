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

    # Check if user added 'help'
    if len(sys.argv) > 0:
        if sys.argv[0] == "help":
            print("Usage: python script.py <file_path> <output_file> <PARX> <timeOut>")
            sys.exit(1)
    #Get input data from user
    file_path_raw = input("Enter file path of raw.csv: ")
    folder_path = os.path.dirname(file_path_raw)
    output_folder = input("Enter path of output directory: ")
    problem_name = input("Enter the name of the problem used in probo2 (e.g. DS-PR): ")
    benchmark_name = input("Enter the name of the benchmark set used in probo2 (e.g. ICCMA23): ")
    input_cores = input("Enter number of cores (incrementing) used by the solvers, seperated by ' ':")
    slvrs_cores = list(map(int,input_cores.split(' ')))
    """ #DEBUG ========================================================
    print("slvrs_cores: " + str(slvrs_cores))
    #============================================================== """

    dataframe = read_csv_to_dataframe(file_path_raw)
    """ #DEBUG ========================================================
    print(dataframe)
    #============================================================== """
    # Group DataFrame by the "name" column
    grouped_df_solvers = dataframe.groupby("solver_name")
    
    # get array holding all names of the solvers
    names_solvers = list(grouped_df_solvers.groups.keys())
    """ #DEBUG ========================================================
    print("names_solvers: " + str(names_solvers))
    #============================================================== """
    #create array holding paths to the output files of a solver
    
    path_slvr_out_file = os.path.join(folder_path, names_solvers[0],problem_name, benchmark_name)
    """ #DEBUG ========================================================
    print(path_slvr_output)
    #============================================================== """

    #iterate through instances
    csv_data = []
    for file_instance in os.listdir(path_slvr_out_file):
        filename_out_file = os.fsdecode(file_instance)
        name_instance = filename_out_file[:filename_out_file.rindex('_')]
        """ #DEBUG ========================================================
        print(filename_out_file)
        #============================================================== """
        # read nb_args after COI
        file_path_out_file = os.path.join(path_slvr_out_file, filename_out_file)
        with open(file_path_out_file) as file:
            tmp_lines = file.readlines()
            if len(tmp_lines) == 0:
                nb_args_after_coi = 0
            else:
                nb_args_after_coi = int(tmp_lines[-1])
            """ #DEBUG ========================================================
            print("nb_args_after_coi: " + str(nb_args_after_coi))
            #============================================================== """
        #check if args == 0, skip instances solves during preprocessing
        if nb_args_after_coi == 0:
            continue
        # for each instance compare RT for different solvers
        df_instances = dataframe.loc[dataframe['instance'] == name_instance]
        """ #DEBUG ========================================================
        print(df_instances)
        #============================================================== """
        # choose solver with minimum RT
        df_instances_min = df_instances[df_instances.runtime == df_instances.runtime.min()]
        tmp_solver_name = df_instances_min.iloc[0]['solver_name']
        """ #DEBUG ========================================================
        print(df_instances_min)
        #============================================================== """
        # calculate nb_args/nb_cores
        nb_cores = slvrs_cores[names_solvers.index(tmp_solver_name)]
        """ #DEBUG ========================================================
        print("nb_cores: " + str(nb_cores))
        #============================================================== """
        # save in csv_data: instance_name, nb_args_after_coi, nb_cores
        runtime_instance = df_instances_min.iloc[0]['runtime']
        if not csv_data:
            csv_data = [{'instance' : name_instance, 'nb_args_after_coi' : nb_args_after_coi, 'nb_cores' : nb_cores, 'solver_name': tmp_solver_name, 'runtime': runtime_instance}]
        else:
            csv_data.append({'instance' : name_instance, 'nb_args_after_coi' : nb_args_after_coi, 'nb_cores' : nb_cores, 'solver_name': tmp_solver_name, 'runtime': runtime_instance})
        """ #DEBUG ========================================================
        print("csv_data: " + str(csv_data))
        sys.exit(1)
        #============================================================== """
    
    #write csv file
    path_csv_file = os.path.join(output_folder, 'analysis_CvsRT.csv')
    with open(path_csv_file, 'w', newline='') as csvfile:
        fieldnames = ['instance', 'nb_args_after_coi', 'nb_cores', 'solver_name', 'runtime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)       
    