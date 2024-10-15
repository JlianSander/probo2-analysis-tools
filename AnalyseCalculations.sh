#!/usr/bin/bash
#set -x

#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- PARAM ----////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

#number of instances in the directory, which were taken into account
num_instances=0
#sum of all calculations over the observed instances
num_calculations=0
#sum of all elements in a queue in all instances observed
num_elements_in_queue=0
#sum of all elements processed in all instances observed
num_elements_processed=0
#sum of all attemps to add an element to the queue in all instances observed
num_elements_tried_add=0

#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- MAIN ----/////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

if [ -z "$1" ]
  then
    echo "Path to the directory: "
    read dir
else
    dir=$1
fi
# Check if the target is a directory
if [ ! -d "$dir" ]; then
    echo "$dir"
    echo "Path does not lead to a directory"
    exit 1
fi

#iterate through files
for FILE in "$dir"/*; do 
    #read result
    result=$(sed '2q;d' < $FILE)
    if [ "$result" = "NO" ]; then
        num_calculations_tmp=$(sed '4q;d' < $FILE)

        if [ "$num_calculations_tmp" = "0" ]; then
            #do not take instances into account which have been solved without compution, e.g. by preprocessor
            continue
        else
            if (( num_calculations_tmp > 1 )); then
                path=$(sed '1q;d' < $FILE)
                echo "$path                                                 $num_calculations_tmp calculations"
            fi
        fi

        ((num_instances++))
        num_elements_in_queue_tmp=$(sed '6q;d' < $FILE)
        num_elements_processed_tmp=$(sed '8q;d' < $FILE)
        num_elements_tried_add_tmp=$(sed '10q;d' < $FILE)
        num_calculations=$((num_calculations+num_calculations_tmp))
        num_elements_in_queue=$((num_elements_in_queue+num_elements_in_queue_tmp))
        num_elements_processed=$((num_elements_processed+num_elements_processed_tmp))
        num_elements_tried_add=$((num_elements_tried_add+num_elements_tried_add_tmp))
    fi
done

num_calc_per_inst=$((num_calculations/num_instances))
num_elem_per_inst=$((num_elements_in_queue/num_instances))
num_proc_per_inst=$((num_elements_processed/num_instances))
num_add_per_inst=$((num_elements_tried_add/num_instances))
echo "Number of instances counted                                       $num_instances"
echo "Average number of all calculations per solved instance            $num_calc_per_inst" 
echo "Average number of elements in queue per instance                  $num_elem_per_inst"
echo "Average number of processed elements per instance                 $num_proc_per_inst"
echo "Average number of elements tried to add                           $num_add_per_inst"