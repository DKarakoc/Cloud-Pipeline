import abc


class IStorageClientWrapper(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def download_from_storage_client(self, **kwargs):
        raise NotImplementedError("User of this abstract class must implement this method.")

    @abc.abstractmethod
    def upload_to_storage_client(self, **kwargs):
        raise NotImplementedError("User of this abstract class must implement this method.")

    @abc.abstractmethod
    def show_files_stored_by_storage_client(self):
        raise NotImplementedError("User of this abstract class must implement this method.")

    @abc.abstractmethod
    def delete_file_managed_by_storage_client(self, **kwargs):
        raise NotImplementedError("User of this abstract class must implement this method.")

    @abc.abstractmethod
    def generate_json_upload_parameters(self, **kwargs):
        raise NotImplementedError("User of this abstract class must implement this method.")
