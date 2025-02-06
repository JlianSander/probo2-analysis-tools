import os

def write_arg_to_file(path, file_name, name_ext, argument):
    filename_output = os.path.join(path,file_name + '.' + name_ext)
    f = open(filename_output, "w")
    f.write(str(argument))
    f.close()


input_folder = input("Enter path of the directory containing files to change: ")
name_ext_old = input("Enter the file ending of the files: .")
name_ext_new = input("Enter the new file ending: .")
# iterate through files in folder
for file_input in os.listdir(input_folder):
    filename_input = os.fsdecode(file_input)
    file_path_input = os.path.join(input_folder, filename_input)
    """ #DEBUG ========================================================
    print(filename_input)
    print(file_path_input)
    #============================================================== """
    # check if file is containing labels, if not skip file
    if not(file_input.endswith('.' + name_ext_old)):
        """ #DEBUG ========================================================
        print("not the correct ending")
        #============================================================== """
        continue
    new_filename_path = file_path_input.strip('.' + name_ext_old) + '.' + name_ext_new
    os.rename(file_path_input, new_filename_path)

    #TODO character 'f' before ending gets deleted