#!/usr/bin/bash
#set -x

#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- PARAM ----////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

num_instances=0
num_instances_empty=0

#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- MAIN ----/////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

echo "Version 1.1"
echo "created by Julian Sander"

if [ "$#" -ne 5 ]
  then
    echo "copyEmpty [path out files] [path files af/arg] [path destination] [file ending af] [file ending arg]"
    exit 1    
fi

dir_1=$1
dir_2=$2
dir_3=$3

#iterate through .out files
for FILE in "$dir_1"/*.out; do 
    ((num_instances++))
    result_1=$(sed {1"q;d"} < $FILE)
    if [ -z "$result_1" ]; then
        #echo "Empty File: $FILE"
        ((num_instances_empty++))

        FILE_BASENAME=$(basename -- "$FILE")
        FILE_BASENAME="${FILE_BASENAME%_1.*}"
        #echo "$FILE_BASENAME"
        
        FILE_AF=$(find $dir_2 -name "${FILE_BASENAME}.$4")
        cp "$FILE_AF" "$dir_3/"

        FILE_ARG=$(find $dir_2 -name "${FILE_BASENAME}.$5")
        cp "$FILE_ARG" "$dir_3/"
    fi
done

echo "Empty files:                      $num_instances_empty/$num_instances"