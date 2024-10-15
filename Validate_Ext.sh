#!/usr/bin/bash
#set -x

#input arg-File
if [ -z "$1" ]
  then
    echo -e "\nPath to the .arg-File of the problem: "
    read file_out
else
    file_arg=$1
fi
# Check input fpr .arg-File
if [ ! -f "$file_arg" ]; then
    echo "$file_arg"
    echo "ERROR:    Path does not lead to a file"
    exit 1
elif [[ "${file_arg: -4}" == "{.arg}" ]]; then
    echo "$file_arg"
    echo "ERROR:    File is not of format .arg"
    exit 1
fi

#input i23-File
if [ -z "$2" ]
  then
    echo "Path to the .i23-File of the problem: "
    read file_i23
else
    file_i23=$2
fi

# Check input fpr .i23-File
if [ ! -f "$file_i23" ]; then
    echo "$file_i23"
    echo "ERROR:    Path does not lead to a file"
    exit 1
elif [[ "${file_i23: -4}" == "{.i23}" ]]; then
    echo "$file_i23"
    echo "ERROR:    File is not of format .i23"
    exit 1
fi

#input out-File
if [ -z "$3" ]
  then
    echo -e "\nPath to the .out-File of the solution: "
    read file_out
else
    file_out=$3
fi

# Check input fpr .out-File
if [ ! -f "$file_out" ]; then
    echo "$file_out"
    echo "ERROR:    Path does not lead to a file"
    exit 1
elif [[ "${file_out: -4}" == "{.out}" ]]; then
    echo "$file_out"
    echo "ERROR:    File is not of format .out"
    exit 1
fi

if [ -z "$4" ]
  then
    print_console=false
else
    print_console=$4
fi

#parse query
while IFS="" read -r line || [ -n "$line" ]
do
    if [[ -n "${line// /}" ]]; then
        query=$line
        break
    fi
done < $file_arg
#echo "Query: $query"

#parse extension into one line
raw_ext=$(sed -n '2,${p;}' < $file_out) 
extension=$(echo $raw_ext | sed s/'\r'//g)

is_Valid=false
#iterate through extension
for ext in $extension; do
    if [[ "$ext" == *"w"* ]]; then
        continue
    fi

    #echo "Argument of Extension: $ext"; 

    #iterate through i23-File
    while IFS="" read -r line || [ -n "$line" ]
    do
        #check for ext attacking arg
        if [[ "$line" == *"$ext $query"* ]]; then
            echo $line
            is_Valid=true
            break
        fi
    done < $file_i23   
    
    if [ "$is_Valid" = true ]; then
        break
    fi
done

if [ "$print_console" = true ]; then
    if [ "$is_Valid" = true ]; then
        echo "Valid"
    else
        echo "Invalid"
    fi
fi

