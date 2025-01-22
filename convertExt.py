import os

def write_arg_to_file(path, file_name, name_ext, argument):
    filename_output = os.path.join(path,file_name + '.' + name_ext)
    f = open(filename_output, "w")
    f.write(str(argument))
    f.close()


input_folder = input("Enter path of the directory containing the files of the additional (query) arguments for DS/DC problems: ")
name_ext_old = input("Enter the existing file ending of the additional arguments:")
name_ext_new = input("Enter the new file ending of the additional arguments:")
wrapping_argument = input("Enter any symbols that are used to describe the argument, apart of its number. (e.g. 'a'):")
# iterate through files in folder
for file_input in os.listdir(input_folder):
    filename_input = os.fsdecode(file_input)
    file_path_input = os.path.join(input_folder, filename_input)
    """ #DEBUG ========================================================
    print(filename_input)
    print(file_path_input)
    #============================================================== """
    # check if file is containing labels, if not skip file
    if not(filename_input.endswith('.' + name_ext_old)):
        """ #DEBUG ========================================================
        print("not a label")
        #============================================================== """
        continue
    name_instance = filename_input.strip('.' + name_ext_old)
     # open file and read argument
    with open(file_path_input) as file:
        tmp_lines = file.readlines()
        if len(tmp_lines) != 0 and not tmp_lines[0].isspace():
            arg_str = tmp_lines[0]
            arg_int = int(arg_str.strip(wrapping_argument))
            """ #DEBUG ========================================================
            print("Argument: " + str(arg_int))
            #============================================================== """
             # write argument in file
            write_arg_to_file(input_folder, name_instance, name_ext_new, arg_int)