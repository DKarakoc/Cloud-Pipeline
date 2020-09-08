# Main Class for the Application library.
import os
from .Models.Handler.ClientWrapperHandler import ClientWrapperHandler
from .Models.Clients.ClientType import ClientType


def download_from_cloud(**kwargs):
    """
    Downloads a stored Blob (file or directory) inside the secure TKH Google Cloud environment (aka bucket).

     Args:
            destination (str):
                Directory on local system to which to download the blob.
            folder_path (str):
                TODO: write documentation
            bucket_name (str):
                TODO: write documentation
            storage_retrieval_script_path (str):
                Optional - TODO: write documentation
            blob_name (str):
                TODO: write documentation

        Returns:
            Void - Downloads file to local directory instead.
    """

    main_handler = ClientWrapperHandler(ClientType.Google, os.getcwd())
    main_handler.download_from_client(**kwargs)


def show_files_in_cloud_directory():
    """
    Shows the files currently held within the default project Google Cloud bucket.

        Returns:
            Void - Outputs the bucket/blob list to the console.
    """

    main_handler = ClientWrapperHandler(clientType=ClientType.Google, prj_root_dir=os.getcwd())
    main_handler.show_files_stored_by_client()


def delete_dir_from_cloud_directory(**kwargs):
    """
    Downloads a stored Blob (file or directory) inside the secure TKH Google Cloud environment (aka bucket).

     Args:
            bucket_name (str):
                TODO: write documentation
            blob_name (str):
                TODO: write documentation

        Returns:
            Void - Downloads file to local directory instead.

        Raises:
              ValueError if the target bucket/blob do not exist.
    """

    main_handler = ClientWrapperHandler(ClientType.Google, os.getcwd())
    main_handler.delete_file_managed_by_client(**kwargs)


def upload_to_cloud(**kwargs):
    """
    Downloads a stored Blob (file or directory) inside the secure TKH Google Cloud environment (aka bucket).

     Args:
            destination (str):
                Directory on local system to which to download the blob.
            folder_path (str):
                TODO: write documentation
            bucket_name (str):
                TODO: write documentation
            storage_retrieval_script_path (str):
                Optional - TODO: write documentation
            blob_name (str):
                TODO: write documentation

        Returns:
            Void - Downloads file to local directory instead.
    """

    main_handler = ClientWrapperHandler(ClientType.Google, os.getcwd())
    main_handler.upload_to_client(**kwargs)


def download_from_local_storage(**kwargs):
    """
    Retrieving a file/folder from local storage,
    i.e. moving a file/folder from the current directory to the desired directory
    :param source_path: source directory from which the file should be retrieved
    :param kwargs:
        optional - destination_path: the destination directory for the file/folder
                                if not provided, the destination will be self.path
        optional - decompression (bool) : decompress yes or no.
    :return: does not return anything
    """

    main_handler = ClientWrapperHandler(ClientType.Local, os.getcwd())
    main_handler.download_from_client(**kwargs)


def show_files_in_local_storage_directory():
    """
    Example description TODO: write documentation

     Args:
            ex1 (str/bool/dict):
                example description TODO: write documentation

        Returns:
            Void - TODO: write documentation

        Raises:
            TODO: write documentation
    """

    main_handler = ClientWrapperHandler(ClientType.Local, os.getcwd())
    main_handler.show_files_stored_by_client()


def delete_dir_from_show_files_in_local_storage(**kwargs):
    """
    Example description TODO: write documentation

     Args:
            ex1 (str/bool/dict):
                example description TODO: write documentation

        Returns:
            Void - TODO: write documentation

        Raises:
            TODO: write documentation
    """

    main_handler = ClientWrapperHandler(ClientType.Local, os.getcwd())
    main_handler.delete_file_managed_by_client(**kwargs)


def upload_to_local_storage(**kwargs):
    """
        Store a file/folder to a desired directory in the local storage
            :param source_path: current directory of the file
            :param destination_path: destination directory where the file/folder should be moved to
            :param kwargs:
                optional - compression_alg: if compression is true, the file/folder will be compressed before saving
                optional - intended_stored_file_name: the name you want to give the compressed file/folder,
                           if not given a default name will be given
    """

    main_handler = ClientWrapperHandler(ClientType.Local, os.getcwd())
    main_handler.upload_to_client(**kwargs)
