import os
import aspose.words as aw

def GetFileName(file_path):
    return file_path.split('/')[-1]

def RemoveFileTypeExtention(file_name):
    return file_name.split('.')[0]

def ConvertWordFileToTxt(input_file_name, output_file_name):
    doc = aw.Document(input_file_name)
    doc.save(output_file_name)

def ConvertWordFilesToTxtFiles(input_files_directory_path, output_files_directory_path):
    input_directory = os.fsencode(input_files_directory_path)
    for file in os.listdir(input_directory):
        filename = os.fsdecode(file)
        if filename.endswith(".doc") or filename.endswith(".docx"):
            doc = aw.Document(input_files_directory_path + "/" + filename)
            doc.save(output_files_directory_path + "/" + filename.split(".")[0]+".txt")
        else: 
            continue