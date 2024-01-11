#!/bin/bash

ollama_list_output=$(ollama list)

if [ $? -ne 0 ]; then
    echo "Error running 'ollama list'. Make sure ollama is installed and configured correctly."
    exit 1
fi

options=$(echo "$ollama_list_output" | awk 'NR>1 {printf "%s:%s ", $1, $2}')

IFS=' ' read -r -a options_array <<< "$options"

echo "Select a model to launch:"
select model_option in "${options_array[@]}"; do
    if [[ -n $model_option ]]; then
        model_name=$(echo "$model_option" | cut -d':' -f1)
        
        ollama run "$model_name"
        break
    else
        echo "Invalid option. Please select a valid option."
    fi
done
