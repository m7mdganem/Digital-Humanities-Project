from glob import glob
import os
import re
import os
import win32com.client as win32
import pypandoc
from win32com.client import constants

def GetFileName(file_path):
    return file_path.split('/')[-1]

def RemoveFileTypeExtention(file_name):
    return file_name.split('.')[0]

def ConvertWordFilesToTxtFiles(input_files_directory_path, output_files_directory_path):
    input_directory = os.fsencode(input_files_directory_path)
    for file in os.listdir(input_directory):
        filename = os.fsdecode(file)
        if filename.endswith(".docx"):
            ConvertDocxToTxt(input_files_directory_path + "/" + filename, output_files_directory_path + "/" + filename.split(".")[0]+".txt")
        else: 
            continue

def ConvertDocxToTxt(filename, outputFileName):
    pypandoc.convert_file(filename, 'plain', outputfile=outputFileName, encoding="utf-8")

def ConvertDocFilesToDocx(path_to_doc_files):
    # Create list of paths to .doc files
    paths = glob(path_to_doc_files + '\\**\\*.doc', recursive=True)
    for path in paths:
        _save_as_docx(path)

def _save_as_docx(path):
    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate ()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)