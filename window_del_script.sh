#!/bin/bash

# The path to the file and directories to be deleted.
# Update these paths to the locations of the items you want to delete.
file_to_delete="Memory_dump"
directory_to_delete1="Carved"
directory_to_delete2="Pytsk_Carved"

# Delete the file
if [[ -f "$file_to_delete" ]]; then
    rm -f "$file_to_delete"
    echo "File $file_to_delete deleted."
else
    echo "File $file_to_delete does not exist."
fi

# Delete the first directory
if [[ -d "$directory_to_delete1" ]]; then
    rm -rf "$directory_to_delete1"
    echo "Directory $directory_to_delete1 deleted."
else
    echo "Directory $directory_to_delete1 does not exist."
fi

# Delete the second directory
if [[ -d "$directory_to_delete2" ]]; then
    rm -rf "$directory_to_delete2"
    echo "Directory $directory_to_delete2 deleted."
else
    echo "Directory $directory_to_delete2 does not exist."
fi
