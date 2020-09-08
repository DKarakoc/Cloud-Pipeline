from Models.Interfaces.IStorageClientWrapper import IStorageClientWrapper


class AmazonCloudClientWrapper(IStorageClientWrapper):

    def __init__(self):
        raise NotImplementedError("class not implemented")

    def show_files_stored_by_storage_client(self):
        raise NotImplementedError("class not implemented")

    def delete_file_managed_by_storage_client(self, **kwargs):
        raise NotImplementedError("class not implemented")

    def upload_to_storage_client(self, **kwargs):
        raise NotImplementedError("class not implemented")

    def download_from_storage_client(self, **kwargs):
        raise NotImplementedError("class not implemented")

    def __generate_json_upload_parameters(self, **kwargs):
        raise NotImplementedError("User of this abstract class must implement this method.")