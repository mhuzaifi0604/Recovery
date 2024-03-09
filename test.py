import os
os.environ['MAGIC'] = 'C:\\Windows\\System32\\magic1.dll'
import magic

# Define the directory to perform file carving
target_directory = 'E:\\Recovery'

# Create a directory to save recovered files
recovery_directory = 'E:\\Recovered'
os.makedirs(recovery_directory, exist_ok=True)

# Initialize the magic library
magic_instance = magic.Magic()

# Function to check if a file is a text file
def is_text_file(file_path):
    mime_type = magic_instance.from_file(file_path)
    return mime_type.startswith('text/')

# Iterate through all entries in the target directory
for root, dirs, files in os.walk(target_directory):
    for file_name in files:
        file_path = os.path.join(root, file_name)

        if is_text_file(file_path):
            # This is a text file, you can process and recover it
            with open(file_path, 'rb') as source_file:
                file_data = source_file.read()
                recovered_path = os.path.join(recovery_directory, file_name)
                with open(recovered_path, 'wb') as recovered_file:
                    recovered_file.write(file_data)

# Once the script is executed, check the recovery directory for any recovered text files
