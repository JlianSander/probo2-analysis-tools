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

def get_num_args(input_folder_frameworks, name_instance):
    file_path_framework = os.path.join(input_folder_frameworks, name_instance + ".i23")
    with open(file_path_framework) as file_framework:
        line_tmp = file_framework.readline().strip(' p ').strip(' af ').strip(' aba ')
        line_tmp = line_tmp.strip() # removes whitespaces
        return int(line_tmp)

input_folder = input("Enter path of the directory containing the label files: ")
input_folder_frameworks = input("Enter path of the directory containing the .i23 files: ")
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
        if len(tmp_lines) != 0 and not tmp_lines[0].isspace():
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
                arg_int = int(line.strip("a"))
                list_accepted.append(arg_int)
            # save int in list and output args not in list but lower than max arg in list as "not accepted"
            list_accepted.sort(reverse=True)
            arg_max = list_accepted[0]
            """ #DEBUG ========================================================
            print("arg_max: " + str(arg_max))
            print("list_accepted: " + str(list_accepted))
            #============================================================== """
            has_empty_slot = False
            for i in range(arg_max - 1):
                if not(list_accepted.__contains__(i)):
                    has_empty_slot = True
                    break
            if has_empty_slot and arg_max > 1:
                # generate random argument and check if it is accepted
                arg_not_accepted = random.randint(1, arg_max - 1)
                while list_accepted.__contains__(arg_not_accepted):
                    arg_not_accepted = random.randint(1, arg_max - 1)
                # write argument in file in subfolder of rejected arguments
                write_arg_to_file(path_subfolder_rejected, name_instance, arg_not_accepted)
            else:
                # check if arg_max is highest argument in the framework
                num_args = get_num_args(input_folder_frameworks, name_instance)
                """ #DEBUG ========================================================
                print("num_args: " + str(num_args))
                #============================================================== """
                if arg_max < num_args:
                    # there are arguments higher than arg_max in the framework, take next one higher as rejected
                    write_arg_to_file(path_subfolder_rejected, name_instance, arg_max + 1)
        else:
            #no argument was labelled as accepted
            num_args = get_num_args(input_folder_frameworks, name_instance)
            arg_not_accepted = random.randint(1, num_args)
            write_arg_to_file(path_subfolder_rejected, name_instance, arg_not_accepted)
                

            
            
