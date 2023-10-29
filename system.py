import psutil

def get_file_system(mypath):
    file_system = ""
    for partition in psutil.disk_partitions():
        if partition.mountpoint == '/':
            file_system = partition.fstype
            continue

        if mypath.startswith(partition.mountpoint):
            return partition.fstype

    return file_system

path = str(input("Enter the path to file system Directory: "))
valid_path = path.replace("\\", "\\\\")
print(f"Detected File System for '{path}' is: ", get_file_system(valid_path))