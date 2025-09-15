#!/usr/bin/bash
#set -x

echo "analyseResults v1.1"
echo "created by Julian Sander"

if [ "$#" -ne 1 ]
  then
    echo "analyseResults.sh [INPUT folder .out files]"
    exit 1    
fi

dir_1=$1

# init variables to count files
    num_instances=0
    num_instances_empty=0
    num_instances_yes=0
    num_instances_no=0

for FILE in "$dir_1"/*.out; do 
    ((num_instances++))
    result_1=$(sed {1"q;d"} < $FILE)
    if [ -z "$result_1" ]; then
        #echo "Empty File: $FILE"
        ((num_instances_empty++))
    else
        #echo "Not Empty: $FILE"
        if [ "$result_1" = "YES" ]; then
            ((num_instances_yes++))
        fi
        if [ "$result_1" = "NO" ]; then
            ((num_instances_no++))
        fi
    fi
done

echo "Number instances:               $num_instances"  
echo "Empty files:                    $num_instances_empty"
echo "NO result:                      $num_instances_no"
echo "YES result:                     $num_instances_yes"
       