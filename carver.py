import os
import psutil
import pytsk3
import subprocess

def get_file_system(mypath):
    file_system = ""
    for partition in psutil.disk_partitions():
        if partition.mountpoint == '/':
            file_system = partition.fstype
            continue

        if mypath.startswith(partition.mountpoint):
            return partition.fstype

    return file_system

def find_process_id(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return "Process not found"

def capture_mem_dump_for_linux(path, output_dump):
    # with open(path, 'rb') as disk:
    #     sector = disk.read(2048)
    #     with open(output_dump, 'wb') as dump:
    #         dump.write(sector)
    dd_command = ['sudo', 'dd', f'if={path}', f'of={output_dump}', 'bs=1M', 'conv=noerror,sync', 'count=1']

    print("Adding dump to the memdump file")
    try:
        subprocess.run(dd_command, check=True)
        print(f"Memory dump saved to {output_dump}")
    except subprocess.CalledProcessError as error:
        print(f"Error capturing memory dump: {error}")

def capture_mem_dump_for_windows(path, output_dump):
    command = ['./dd.exe', f'if={path}', f'of={output_dump}', 'bs=1M', 'count=1']
    print("adding dump to the memdump file")
    try:
        subprocess.run(command, check=True)
        print(f"Memory dump saved to {output_dump}")
    except subprocess.CalledProcessError as error:
        print(f"Error capturing memory dump: {error}")


def recover_del_files_using_pytsk(path, output_dir):
    print("=========================================\n Getting Image Info\n")
    img_info = pytsk3.Img_Info(path)
    filesystem = pytsk3.FS_Info(img_info)
    for roor, _, files in file_system:
        for file in files:
            print("Reading file in dir")
            file_inode = file.info.meta.addr
            if file_inode in range(11, 1000):
                print("Checking file inode between 11 and 1000")
                file_data = file_system.open_meta(inode=file_inode)
                print("Reading file data")
                data = file_data.read_random(0, file_data.info.meta.size_of_a_sector)
                filename = f"{file_inode}_{file.info.__name__}"
                file_output_path = os.path.join(output_dir, filename)
                with open(file_output_path, 'wb') as recovered_file:
                    print("Writing to file")
                    recovered_file.write(data)
                print("=========================================")


def recover_from_mem_dump(extension):
    print("recovering from memdump")
    with open("Memory_dump", 'rb') as f:
        print("reading memdump")
        dump = f.read()
    signature = re.compile(rb'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', re.DOTALL)
    matches = re.finditer(signature, dump)
    for match in matches:
        data = match.group(0)
        print("Matching file > 500 in memdump")
        if len(data) > 500:
            with open(f"Recovered_file.{extension}", "wb") as recovered:
                recovered.write(data)
                print("Recovered file")


def carve_files(path, output_dir):
    for root, dir, files in os.walk(path):
        start = 0
        for file in files:
            file_path = os.path.join(root, file)
            print("=========================================")
            with open(file_path, 'rb') as f:
                print("Readingfiles as binary")
                file_data = f.read()
                # recovered_path = os.path.join(output_dir, file)
                # with open(recovered_path, 'wb') as recovered_file:
                #     recovered_file.write(file_data)
            signature = b'\x4c\x69\x76'
            
            print("starting looking for text doc")
            while True:
                print ("Looking via signature")
                start = file_data.find(signature, start)
                if start == -1:
                    print ("No signature found")
                    break
                end = file_data.find(b'\x0a', start)
                if end == -1:
                    print ("No end found")
                    break
                print ("Found a text file")
                data = file_data[start:end]
                filename = f"{start}_{end}.txt"
                start = end + 1
                file_output_path = os.path.join(output_dir, filename)
                with open(file_output_path, 'wb') as recovered_file:
                    print ("Writing to file")
                    recovered_file.write(data)
                print("========================================")

if __name__ == "__main__":
    path = input("enter the target path: ")
    output_dir = "Carved"
    output_dump = "Memory_dump"
    pytsk_output_dir = "Pytsk_Carved"
    valid_path = path.replace("//", "////")

    file_system = get_file_system(valid_path)
    print("File System: ", file_system, "\n")

    print("Valid Path: ", valid_path)
    if not os.path.exists(output_dir):
        print("Creating directory!")
        os.makedirs(output_dir)

    if not os.path.exists(pytsk_output_dir):
        print("Creating PyTsk directory!")
        os.mkdir(pytsk_output_dir)

    carve_files(valid_path, output_dir)
    # recover_del_files_using_pytsk(valid_path, pytsk_output_dir)
    if file_system.lower() == 'ext4':
        print("EXT4 File System Mem Dump Collection")
        pid = find_process_id("file_carver.py")
        if pid != "Process not found":
            print("Process Found: ", pid)
            # handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
            # win32api.TerminateProcess(handle, -1)
            # win32api.CloseHandle(handle)
            capture_mem_dump_for_linux("/dev/sdc", output_dump)
            recover_from_mem_dump("png")
        else:
            print("Process not found!")
            capture_mem_dump_for_linux("/dev/sdc", output_dump)
    elif file_system == 'NTFS' or file_system == 'FAT32':
        capture_mem_dump_for_windows("\\\\.\\E:", output_dump)
        print("File System is NTFS")
    else:
        print("File System not supported")

