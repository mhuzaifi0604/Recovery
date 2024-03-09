import os
import psutil
import pytsk3
import tempfile

def get_file_system(mypath):
    file_system = ""
    for partition in psutil.disk_partitions():
        if partition.mountpoint == '/':
            file_system = partition.fstype
            continue

        if mypath.startswith(partition.mountpoint):
            return partition.fstype

    return file_system

def create_disk_image(disk_image, size_in_bytes):
    # with open(path, "r") as read_path:
    #     with open(disk_image, "wb") as files:
    #         while True:
    #             if files.write(read_path.read(size)) == 0:
    #                 break

    with open(disk_image, 'wb') as f:
        f.seek(size_in_bytes - 1)
        f.write(b'\x00')



def create_forensic_disk_image(dir_path, dd_image):
    image_info = pytsk3.Img_Info(dd_image)
    volume_info = pytsk3.Volume_Info(image_info)
    print("Volume Info: ", volume_info.info)
    with open(dd_image, "wb") as image_file:
        file_system = pytsk3.FS_Info(image_file)
    #     root_directory = file_system.open_dir(path=dir_path)
    #     for root, _, files in os.walk(directory_path):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             with open(file_path, "rb") as input_file:
    #                 for data in input_file:
    #                     image_file.write(data)
        for dir in file_system.open_dir(path=dir_path):
            for file in dir:
                try:
                    if not file.info.name or file.info.meta:
                        continue
                    file_path = dir_path.join([file.info.name.name.decode("utf-8")])
                    print("File Path: ", file_path)
                    file_data = file.read_random(0, file.info.meta.size)
                    if file_data:
                        image_file.write(file_data)
                except Exception as error:
                    print("Error Reading File: ", error)

# def recovery():
#     try:
#         img = pytsk3.Img_Info("Path_Image.dd")
#         file_system = pytsk3.FS_Info(img).info
#         root = file_system.open_dir(path="./")
        
#         for entry in root:
#             if entry.info.name.name and entry.info.meta.flags:
#                 if pytsk3.TSK_FS_META_FLAG_ALLOC:
#                     recovered_file_name = entry.info.name.name.decode("utf-8")
#                     with open(recovered_file_name, "wb") as recovery:
#                         filedata = entry.read_random(0, entry.info.meta.size)
#                         recovery.write(filedata)
#                     print("Recovered File name:", recovered_file_name)
    
#     except Exception as e:
#         print("An error occurred:", str(e))



# def create_forensic_disk_image(directory_path, output_image_path):
#     # Open the output image using Pytsk3
#     img = pytsk3.Img_Info(output_image_path)

#     # Create a file system on the output image
#     file_system = pytsk3.FS_Info(img)

#     # Create a root directory on the file system
#     root_directory = file_system.open_dir(path="/")

#     for root, _, files in os.walk(directory_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             with open(file_path, "rb") as input_file:
#                 file_data = input_file.read()
#                 # Create a new file in the file system
#                 new_file = root_directory.open(file)
#                 new_file.write(data=file_data, offset=0)

def main():
    path = input("Enter the path to the directory you want to create an image from: ")
    valid_path = path.replace("\\", "\\\\")

    # Determine the file system of the specified path
    detected_file_system = get_file_system(valid_path)
    print(f"Detected File System for '{valid_path}' is: {detected_file_system}")

    # Specify the path and filename for the empty image
    raw_image = "Forensic_Image.dd"

    # Specify the size of the empty image (adjust as needed)
    size_in_bytes = 1024 # 1 MB

    # Create an empty disk image
    create_disk_image(raw_image, size_in_bytes)
    print(f"Empty disk image created at: {raw_image}")

    # Create a forensic disk image from the specified directory
    create_forensic_disk_image(valid_path, raw_image)
    print(f"Forensic disk image created at: {raw_image}")

if __name__ == "__main__":
    main()



with open(dd_image, "wb") as image_file:
        # Open the storage media
        img_info = pytsk3.Img_Info(dd_image)

        # Create a volume object from the storage media
        volume_info = pytsk3.Volume_Info(img_info)

        # Select the first partition (adjust as needed)
        part_info = volume_info[0]

        # Open the file system on the partition
        fs_info = pytsk3.FS_Info(img_info, offset=part_info.start * 512)

        # Open the root directory
        root_dir = fs_info.open_dir(path=dir_path)

        # Iterate over all files in the directory and its subdirectories
        for file_entry in root_dir:
            if not file_entry.info.name or file_entry.info.meta:
                continue

            # Get the file path and read its data
            file_path = os.path.join(dir_path, file_entry.info.name.name.decode("utf-8"))
            file_data = file_entry.read_random(0, file_entry.info.meta.size)

            # Write the data to the output image
            image_file.write(file_data)

        print(f"Forensic disk image created at: {dd_image}")