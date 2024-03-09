import re
import os

HEADERS = {
    'png':b"\x89PNG\r\n\x1a\n",
    'jpg':b"\xff\xd8\xff",
    'pdf':b"\x25\x50\x44\x46\x2d\x31\x2e\x35\x0a\x25\xe2\xe3\xcf\xd3\x0a",
    'exe':b"\x4d\x5a",
}

FOOTERS = {
    'png':b"\x49\x45\x4e\x44\xae\x42\x60\x82",
    'jpg':b"\xff\xd9",
    'pdf':b"\x0a\x25\x25\x45\x4f\x46",
    'exe':b"\x4c\x1b\x0a\x0d\x0a\x1a\x0a\x00\x00\x00\x00\x00\x00\x00\x00",
}

def recover(path_to_image: str, output_directory: str, file_types: []):
    """ Carves files from an image and saves them to a directory """

    with open(path_to_image, 'rb') as image:
        data = image.read()
        for file_type in file_types:
            pattern = re.escape(HEADERS[file_type]) + b".+?" + re.escape(FOOTERS[file_type])
            matches = re.finditer(pattern, data, re.DOTALL)

            for match in matches:
                start_offset = match.start()
                end_offset = match.end()
                subdata = data[start_offset:end_offset]
                carve_filename = f"Carved_{file_type}_{start_offset}_{end_offset}.{file_type}"

                with open(output_directory + "/" + carve_filename, 'wb') as carve_obj:
                    carve_obj.write(subdata)


    # start_offsets = {} # stores the start offsets of each file type (realtime)
    # end_offsets = {} # stores the end offsets of each file type (realtime)

    # with open(path_to_image, 'rb') as image:
    #     data = image.read(int(1e+10))

    #     for file_type in file_types:
    #         start_offsets[file_type] = [match.start() for match in re.finditer(re.escape(HEADERS[file_type]),data)]
    #         end_offsets[file_type] = [match.start() for match in re.finditer(re.escape(FOOTERS[file_type]),data)]

    #     print(start_offsets)
    #     print(end_offsets)

    #     for key, value in start_offsets.items():
                
    #         for i in range(len(start_offsets[key])):
    #             subdata = data[value[i]: end_offsets[key][i]+2]
    #             carve_filename = "Carve1_"+str(value[i])+"_"+str(end_offsets[key][i])+"."+key
    #             print(carve_filename)
                
    #             with open(output_directory+"/"+carve_filename, 'wb') as carve_obj:
    #                 carve_obj.write(subdata)

    #             i=i+1


if __name__ == "__main__":
    path_to_image = "/home/huzaifi/temp/new.dd"
    output_directory = "/home/huzaifi/recovered"

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    file_types = ['jpg', 'png']

    recover(path_to_image, output_directory, file_types)