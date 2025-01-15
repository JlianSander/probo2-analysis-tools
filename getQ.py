import os
import random

def create_folder(path, name):
    path_subfolder = os.path.join(path, name)
    try:
        os.mkdir(path_subfolder)
    except FileExistsError:
        print(f"Directory '{path_subfolder}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{path_subfolder}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return path_subfolder

def write_arg_to_file(path, file_name, argument):
    filename_output = os.path.join(path,file_name + '.arg')
    f = open(filename_output, "w")
    f.write(str(argument))
    f.close()

input_folder = input("Enter path of the directory containing the label files: ")
output_folder = input("Enter path of the output directory: ")
# create subfolders for accepted args and those which are not
path_subfolder_accepted = create_folder(output_folder, "Accepted")
path_subfolder_rejected = create_folder(output_folder, "Rejected")
# read label files in directory
for file_input in os.listdir(input_folder):
    filename_input = os.fsdecode(file_input)
    file_path_input = os.path.join(input_folder, filename_input)
    """ #DEBUG ========================================================
    print(filename_input)
    print(file_path_input)
    #============================================================== """
    # check if file is containing labels, if not skip file
    if not(filename_input.endswith('_labels.txt')):
        """ #DEBUG ========================================================
        print("not a label")
        #============================================================== """
        continue
    name_instance = filename_input.strip('_labels.txt')
    # open file and read arguments
    with open(file_path_input) as file:
        tmp_lines = file.readlines()
        if len(tmp_lines) != 0:
            arg_str = tmp_lines[0]
            arg_int = int(arg_str.strip("a"))
            """ #DEBUG ========================================================
            print("Argument: " + str(arg_int))
            #============================================================== """
            # write argument in file in subfolder of accepted arguments
            write_arg_to_file(path_subfolder_accepted, name_instance, arg_int)
            # iterate through all labeled arguments and create list with arguments
            list_accepted = list()
            for line in tmp_lines:
                arg_int = int(arg_str.strip("a"))
                list_accepted.append(arg_int)
            # save int in list and output args not in list but lower than max arg in list as "not accepted"
            list_accepted.sort(reverse=True)
            arg_max = list_accepted[0]
            has_empty_slot = False
            for i in range(arg_max - 1):
                if not(list_accepted.__contains__(i)):
                    has_empty_slot = True
                    break
            if has_empty_slot and arg_max > 0:
                # generate random argument and check if it is accepted
                arg_not_accepted = random.randint(0, arg_max - 1 )
                while list_accepted.__contains__(arg_not_accepted):
                    arg_not_accepted = random.randint(arg_max - 1 , 0)
                # write argument in file in subfolder of rejected arguments
                write_arg_to_file(path_subfolder_rejected, name_instance, arg_not_accepted)
                

            
            
