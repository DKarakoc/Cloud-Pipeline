import os

from ..Clients.LocalStorageClientWrapper import LocalStorageClientWrapper
from ..Interfaces import IStorageClientWrapper
from ..Metaclasses.Singleton import Singleton
from ..Clients import ClientType
from ..Clients.GoogleCloudClientWrapper import GoogleCloudClientWrapper
from ...Config.DSNRPConfig import DSNRPConfig


class ClientWrapperHandler(object, metaclass=Singleton):

    def __init__(self, clientType: ClientType, prj_root_dir: str):

        self.__clientType = clientType
        self.__prj_root_dir = prj_root_dir
        self.__dsnrpconfig = DSNRPConfig(prj_root_dir)

        if clientType == ClientType.ClientType.Local:
            self.__client: IStorageClientWrapper = LocalStorageClientWrapper(prj_root_dir)
        else:
            self.__client: IStorageClientWrapper = GoogleCloudClientWrapper(
                self.__dsnrpconfig.getGoogleCloudAPIKeyDir(),
                self.__prj_root_dir)

    # --------- METHODS ----------------
    def download_from_client(self, **kwargs):
        self.__client.download_from_storage_client(**kwargs)

    def show_files_stored_by_client(self):
        """Prints all directories managed by the storage client type to stdout. In case of GoogleClientWrapper; it
        will output the blobs in each bucket. In case of the LocalStorageClientWrapper it will output the managed
        directories and sub-directories/files """

        self.__client.show_files_stored_by_storage_client()

    def delete_file_managed_by_client(self, **kwargs):
        """Deletes a single file or compressed directory from a storage location managed by a storage client"""

        self.__client.delete_file_managed_by_storage_client(**kwargs)

    def create_download_script(self):
        raise NotImplementedError('Creation of Download Script not yet implemented!')

    def upload_to_client(self, **kwargs):
        """Uploads a single file or compressed directory to a storage location managed by a storage client"""
        self.__client.upload_to_storage_client(**kwargs)
