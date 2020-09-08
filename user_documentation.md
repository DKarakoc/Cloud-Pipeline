
# Local Storage Documentation  
## Downloading data  
The *download_from_storage_client* method is used to retrieve a file or folder that is stored in the local storage i.e. the computer that is currently used. For the current location of the file/folder the user can either provide the path to a json file containing the source path, or he/she can simply provide the path directly to the file/folder. Furthermore, the user should provide the destination path, i.e. the directory in which he/she wants to store the file/folder. If no destination path is raised the *destination_path* will be set to the project root directory. If the given destination path does not exist yet, it will be created.  
Furthermore, the user can provide the *decompression* boolean value, which will result in decompressing the folder if *True*.  
Finally, if the file should not be decompressed **and** the *destination_path* is the same as the *source_path*, nothing should happen, because moving a file/folder to a directory in which it already exists would result in an error.  
  
## Uploading data  
  
The *upload_to_storage_client* method is used to store a data file or a folder containing multiple files in a specific directory in the local storage. Two parameters must always be provided for the method to work: the *source_path*, which is a string containing the current location of the file/folder, and the *destination_path*, which is a string containing the directory in which the user wants to store the file or folder in question.  
Optionally, two other parameters can be provided, namely: a boolean value *compression*, which determines whether the folder should be compressed or not, and a string *intended_stored_file_name*, with which the user can provide a name for the file or (compressed) folder.  
As single files cannot be compressed into a zip file, it is checked whether the user wanted to do compression on a single file. If that's the case, a *ValueError* will be raised.  
Compression will be handled by the *compress* method of the compression class.  
Finally, upload parameters are created. These parameters can later on be used to retrieve the stored file again, without the user having to think about which parameters he should provide.  
  
## Deleting data  
Locally stored data can also be deleted. The user simply needs to specify the *target_path*, i.e. the path to the to be deleted data file/folder. If the user wants to delete a complete folder he is asked for confirmation, in case it was not what he/she wanted, to prevent accidentally deleting complete folders.  
  
## Generating json parameter file  
*generate_json_upload_parameters* is used in *upload_to_storage_client*. It generates the parameters that would be needed to retrieve the uploaded file and stores them in a json file. The file can be used as parameter in *download_from_storage_client*.  
  
# Compression  
## compression  
Compression is handled by the *compression* method. The name of the archive file (*zip_name*) and the destination path (*dir_name*) should be provided as parameters. Currently the only option is to compress folders in a zip file, but other compression methods can easily be added.  
## decompression  
Decompression is done by *decompression*. The location of the zip file (*path_to_zip_file*) and the directory to extract to (*directory_to_extract_to*) should be specified by the user. The file will be extracted to the given location, and the original zip file is removed.  
  
# Google Cloud Client  
## Helper methods
Throughout the whole class helper methods are used. These are self-explanatory, and most of them are simply based on Google Cloud's existing methods.
## Downloading
*download_from_storage_client* is used to download data from the storage client, in this case the Google Cloud. The user always must specify a *destination*, containing the path to the location where the data should be stored. There are multiple ways of accessing the desired data. First of all, the user can give the path to an existing storage retrieval script (via *storage_retrieval_script_path*), which uses a json file containing the necessary parameters to download the data. Secondly, if the user does not provide a *storage_retrieval_script_path*, he can provide the path to the folder (*folder_path*) he/she wants to download. If a folder path is not provided either, and nor is a *blob_name*, all files in the bucket will be downloaded. Finally, the user can download a blob by simply providing the *bucket_name* and *blob_name*. 
## Uploading
The *upload_to_storage_client* method is used for uploading to the Google Cloud. The user should specify the directory (*path_of_file_to_be_uploaded*) in which the to be uploaded file is stored. Furthermore, he can optionally provide a *bucket_name*. If the latter is not provided, a default name will be generated. If a bucket with that name does not exist yet, it will also be created automatically. 
After making sure the bucket is there, the file(s) can be uploaded. 
Finally, the metadata is created and stored in a json file, using *generate_json_upload_parameters*. These parameters can later on be used to quickly download the file without having to look up what the parameters are.
## Showing files stored by the client
*show_files_stored_by_storage_client* shows displays all blobs within the wrapper managed bucket.
## Deleting files
*delete_file_managed_by_storage_client* is used to delete a specific blob from the bucket. A *bucket_name* and *blob_name* must be specified. 
## Generating upload parameters
_generate_json_upload_parameters_ is used in _upload_to_storage_client_. It generates the parameters that would be needed to retrieve the uploaded file and stores them in a json file. The file can be used as parameter in _download_from_storage_client_.

