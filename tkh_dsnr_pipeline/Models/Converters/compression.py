import zipfile
import shutil
import os


# make_archive(name for the zip, zip/tar, directory to be zipped)
# We are only using zipfiles though, because our decompression function will need to be reworked again
# zipname is just a string name without the .zip
# 'zip' we dont touch, because the decompress2 doesn't handle .tar
# dir_name is full directory path to be zipped, such as "D://Swdev//Repos//team1920-datastorage//testfolder"
# Output is zip_name.zip at "D://Swdev//Repos//team1920-datastorage"
def compress(zip_name, dir_name):
    shutil.make_archive(zip_name, 'zip', dir_name)


# unzips (path to zip file, directory to unzip to)
# Path to zip file is as "D://Swdev//Repos//team1920-datastorage//" + zip_name + ".zip"
# Directory to extract to is as "D://Swdev//Repos//team1920-datastorage"
# Output is an unzipped file with the path: "Directory_to_extract_to" + zip_name + ".zip"
def decompress(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
    os.remove(path_to_zip_file)
