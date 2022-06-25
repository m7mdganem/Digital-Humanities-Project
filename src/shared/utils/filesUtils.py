def GetFileName(file_path):
    return file_path.split('/')[-1]

def RemoveFileTypeExtention(file_name):
    return file_name.split('.')[0]