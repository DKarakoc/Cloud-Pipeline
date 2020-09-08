import os

from google.cloud.storage import Bucket
from google.cloud import storage
from google.api_core.exceptions import NotFound
from ...Models.Interfaces.IStorageClientWrapper import IStorageClientWrapper
from ..DTOs.CloudStorageMetadataDTO import CloudStorageMetadataDTO
from ...Models.Converters.JSONConverter import deserialize_json_to_object, serialize_object_to_json


class GoogleCloudClientWrapper(IStorageClientWrapper):

    def __init__(self, json_auth_file_path: str, prj_root_dir: str):
        self.__storage_client = storage.Client.from_service_account_json(json_auth_file_path)
        self.__prj_root_dir = prj_root_dir

    # --------- ABSTRACT METHOD IMPLEMENTATIONS ----------------------------------------------
    def download_from_storage_client(self, **kwargs):
        """Instructs the google cloud client to download a by (JSON/user) parameters specified blob from to a
        specified or default bucket. """

        storage_retrieval_script_path = kwargs.get("srs_path")
        folder_path = kwargs.get("folder")
        bucket_name = kwargs.get('bucket')
        blob_name = kwargs.get('blob')
        destination = kwargs.get("download_to")  # path of the dir to download the file too; if this is -
        # specified then it should overwrite the file name identifiers

        if bucket_name is None:
            bucket_name = os.path.split(self.__prj_root_dir)[-1]
            print(bucket_name)

        if storage_retrieval_script_path is not None:
            # download from json file
            with open(str(storage_retrieval_script_path), 'r') as fp:
                json_model: CloudStorageMetadataDTO = deserialize_json_to_object(fp)  # read in the json file
                fp.close()

            file_name = json_model.filename
            blob_name = file_name
            destination_file_name = self.__return_destination(destination, blob_name)

            directory = os.path.split(destination_file_name)[-2]
            dir_exists = os.path.isdir(directory)  # check if the directory exists
            if not dir_exists:  # if directory doesn't exist create it
                os.makedirs(directory)

            self.__download_blob(json_model.bucketname, file_name, destination_file_name)

        elif folder_path is not None:
            # Download all files in a bucket that come from the same folder

            bucket_obj = self.__return_bucket_obj_by_name(bucket_name)

            # get all blob names
            all_blob_names = self.__get_blobs_names_in_bucket(bucket_obj)
            for blob_name in all_blob_names:
                if folder_path in blob_name:
                    destination_file_name = self.__return_destination(destination, blob_name)

                    directory = os.path.split(destination_file_name)[-2]
                    dir_exists = os.path.isdir(directory)  # check if the directory exists
                    if not dir_exists:  # if directory doesn't exist create it
                        os.makedirs(directory)

                    self.__download_blob(bucket_obj, blob_name, destination_file_name)

        elif folder_path is None and blob_name is None:
            # Download all files in bucket

            print("No folder or file specified, downloading all files in bucket: ", bucket_name)
            # if bucket_name is None:
            #     raise ValueError( 'Specify Bucket to download folder from!' )

            bucket_obj = self.__return_bucket_obj_by_name(bucket_name)
            all_blob_names = self.__get_blobs_names_in_bucket(bucket_obj)

            for blob_name in all_blob_names:
                destination_file_name = self.__return_destination(destination, blob_name)

                directory = os.path.split(destination_file_name)[-2]
                dir_exists = os.path.isdir(directory)  # check if the directory exists
                if not dir_exists:  # if directory doesn't exist create it
                    os.makedirs(directory)
                self.__download_blob(bucket_obj, blob_name, destination_file_name)

        else:
            # download by bucket and blob name
            if blob_name is None:
                raise ValueError('Specify file name to download!')

            bucket_obj = self.__return_bucket_obj_by_name(bucket_name)

            destination_file_name = self.__return_destination(destination, blob_name)

            directory = os.path.split(destination_file_name)[-2]
            dir_exists = os.path.isdir(directory)  # check if the directory exists
            if not dir_exists:  # if directory doesn't exist create it
                os.makedirs(directory)

            # self.client.download_blob(bucket_obj, blob_name, destination_file_name)

            bucket = self.__storage_client.get_bucket(bucket_obj)
            blob = bucket.blob(blob_name)

            blob.download_to_filename(destination_file_name)

            print('Blob {} downloaded to {}.'.format(blob_name, destination_file_name))

    def upload_to_storage_client(self, **kwargs):
        """Instructs the google cloud client to upload a user specified blob from to a specified or default bucket."""

        current_bucket_names: [tuple] = [(b.id, b) for b in self.__get_buckets()]

        if current_bucket_names is None:
            raise ValueError('Could not index the current bucket names inside the google cloud!')

        path_of_file_to_be_uploaded = kwargs.get('abs_path_to_file')

        if path_of_file_to_be_uploaded is None:
            raise ValueError('Specify path of the file - or folder - to be uploaded to Google Cloud!')

        bucket_name = kwargs.get('bucket_name')  # see if the user specified a bucket

        bucket = None

        if bucket_name is not None:
            # if a bucket IS specified see if it exists and return the object.
            if self.__check_bucket_exists(bucket_name):
                bucket = self.__return_bucket_obj_by_name(bucket_name)
        else:
            # if a bucket doesn't exists create it from the project root dir
            bucket_name = os.path.split(self.__prj_root_dir)[-1]
            print('When a bucket isn\'t named then the projects root folder will be used as the bucket:',
                  bucket_name)

            bucket_exists = self.__check_bucket_exists(bucket_name)
            if bucket_exists:
                # if the bucket exists return its obj
                bucket = self.__return_bucket_obj_by_name(bucket_name)
            else:
                # if bucket doesn't exists create it
                bucket = self.__storage_client.create_bucket(bucket_name)

        # Now that we have our bucket, we can upload the file(s)
        if os.path.isdir(path_of_file_to_be_uploaded):
            # if the file path is to a folder, upload all files in the folder
            # print("is folder")
            self.__recursive_folder_upload(path_of_file_to_be_uploaded, bucket)
        else:
            to_be_stored_blob_name = kwargs.get('blob_name')

            if to_be_stored_blob_name is None:
                # to_be_stored_blob_name = path_of_file_to_be_uploaded.split( '\\' )[-1]
                filepath = os.path.join(path_of_file_to_be_uploaded)
                to_be_stored_blob_name = filepath.replace(self.__prj_root_dir, "")
                print('User did not set custom file/blob-name to upload under, using default file name: '.format(
                      to_be_stored_blob_name))

            # self.client.upload_blob(bucket, path_of_file_to_be_uploaded, to_be_stored_blob_name)

            # upload_blob:

            if self.__check_bucket_exists(bucket_name):
                bucket = self.__return_bucket_obj_by_name(bucket_name)
            else:
                bucket = self.__storage_client.create_bucket(bucket_name)

            blob = bucket.blob(to_be_stored_blob_name)
            blob.upload_from_filename(path_of_file_to_be_uploaded)
            print('File {} uploaded to {}.'.format(path_of_file_to_be_uploaded, to_be_stored_blob_name))

        # identifiers = to_be_stored_blob_name.split("\\")[:-1]
        metadata = {'project_bucket_name': bucket_name, 'file_name': to_be_stored_blob_name,
                    'generation': self.__getBlobGeneration(bucket, to_be_stored_blob_name),
                    'updated': self.__getBlobUpdated(bucket, to_be_stored_blob_name)}

        self.generate_json_upload_parameters(**metadata)

    def show_files_stored_by_storage_client(self):
        """Instructs the google cloud client to display all blob's within the wrapper managed bucket."""

        all_buckets = list(self.__storage_client.list_buckets())
        for b in all_buckets:
            self.__list_blobs(b)

    def delete_file_managed_by_storage_client(self, **kwargs):
        """Instructs the google cloud client to delete a user specified blob from a bucket."""

        if 'bucket_name' in kwargs:
            bucket_name = kwargs.get('bucket_name')
        else:
            raise ValueError("To delete a file from the google cloud a \'bucket_name\' must be specified.")

        if 'blob_name' in kwargs:
            blob_name = kwargs.get('blob_name')
        else:
            raise ValueError("To delete a file from the google cloud a \'blob_name\' must be specified.")

        bucket_exists = self.__check_bucket_exists(bucket_name)
        if bucket_exists:
            bucket_obj = self.__return_bucket_obj_by_name(bucket_name)
            self.__delete_blob(bucket_obj, blob_name)
        else:
            raise ValueError("Specified deletion bucket or blob target does not exist!")

    def generate_json_upload_parameters(self, **kwargs):
        prj_bucket = kwargs.get("project_bucket_name")
        identifiers = kwargs.get("identifiers")
        file_name = kwargs.get("file_name")
        generation = kwargs.get("generation")
        updated = kwargs.get("updated")

        out_name = os.path.basename(file_name).split(".")[0] + ".json"  # the name of the output json file

        # dir_path = os.path.join( "json files" )  # will return a path for the json files folder
        dir_path = os.path.join(self.__prj_root_dir, "json_files")

        json_model = CloudStorageMetadataDTO(filename=file_name,
                                             bucketname=prj_bucket,
                                             upload_date_time=str(updated),
                                             generationKey=generation)

        if os.path.isdir(dir_path):  # if the folder exists
            with open(os.path.join(dir_path, out_name), 'w') as fp:
                serialize_object_to_json(json_model, fp)
                print("Generated retrieval parameters for file {} in JSON Format. Stored in: {}".format(file_name,
                                                                                                        dir_path))
        else:  # if the folder doesn't exist yet.
            os.makedirs(dir_path)
            with open(os.path.join(dir_path, out_name), 'w') as fp:
                serialize_object_to_json(json_model, fp)
                print("Generated retrieval parameters for file {} in JSON Format. Stored in: {}".format(file_name,
                      dir_path))

    # --------- HELPER METHODS ----------------------------------------------

    def __get_blobs_names_in_bucket(self, bucket: object):
        blobs = self.__get_blobs(bucket)
        return blobs

    def __return_destination(self, destination: str, blob_name: str):
        if destination is not None:
            return os.path.join(destination, os.path.split(blob_name)[-1])
        else:
            return os.path.join(self.__prj_root_dir + blob_name)

    def __get_buckets(self):
        buckets = list(self.__storage_client.list_buckets())
        return buckets

    def __get_bucket(self, bucket: object):
        return self.__storage_client.get_bucket(bucket)

    def __upload_blob(self, bucket: object, source_file_name: str, destination_blob_name: str):
        """Uploads a file to the bucket."""
        bucket = self.__storage_client.get_bucket(bucket)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def __download_blob(self, bucket: object, source_blob_name: str, destination_file_name: str):
        """Downloads a blob from the bucket."""
        bucket = self.__storage_client.get_bucket(bucket)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)

        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))

    def __list_blobs(self, bucket: object):
        """Lists all the blobs in the bucket."""

        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = self.__storage_client.list_blobs(bucket)
        print(bucket, ":")
        for blob in blobs:
            print("\t", blob.name)

    def __get_blobs(self, bucket: object):
        blobs = self.__storage_client.list_blobs(bucket)
        return [blob.name for blob in blobs]

    @staticmethod
    def __delete_blob(bucket: Bucket, blob_name: str):
        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"

        blob = bucket.blob(blob_name)
        try:
            blob.delete()
            print("Blob {} deleted from bucket: {}.".format(blob_name, bucket))
        except NotFound:
            print("File:", blob_name, "doesn't exists in bucket:", bucket)

    @staticmethod
    def __getBlobGeneration(bucket: Bucket, blobName):
        """
        Takes a bucket object and blob name and returns the blobs generation key
        :param self:
        :param bucket: Bucket
        :param blobName: String
        :return:
        """
        return bucket.get_blob(blobName).generation

    @staticmethod
    def __getBlobUpdated(bucket: Bucket, blobName):
        """
        Takes a bucket object and blob name and returns the blobs generation key
        :param self:
        :param bucket: Bucket
        :param blobName: String
        :return:
        """
        return bucket.get_blob(blobName).updated

    # interesting conflict here: method is private, but pycharm suggests it to be static
    # a method is suggested as static when it doesn't use instance variables
    def __getBlobMetadata(self, bucket, blobName: str):
        """Prints a blobs/objects metadata"""
        b = self.__storage_client.get_bucket(bucket)  # get a bucket by name
        blob = b.get_blob(blobName)  # get a blob/object in that bucket by name

        # create object metadata_dict, so you can access these attributes with metadata_dict.blob/.content-type/etc.
        # To easy access to storage, for outside use where template is not available.
        metadata_dict = {"Blob": blob.name, "Bucket": blob.bucket.name, "Storage class": blob.storage_class,
                         "ID": blob.id, "Size (bytes)": blob.size, "Updated": blob.updated,
                         "Generation": blob.generation, "Metageneration": blob.metageneration, "Etag": blob.etag,
                         "Owner": blob.owner, "Component count": blob.component_count, "Crc32c": blob.crc32c,
                         "md5_hash": blob.md5_hash, "Cache-control": blob.cache_control,
                         "Content-type": blob.content_type, "Content-disposition": blob.content_disposition,
                         "Metadata": blob.metadata}

        if blob.temporary_hold:
            metadata_dict["Temporary hold"] = "enabled"
        else:
            metadata_dict["Temporary hold"] = "disabled"
        if blob.event_based_hold:
            metadata_dict["Event based hold"] = "enabled"
        else:
            metadata_dict["Event based hold"] = "disabled"
        if blob.retention_expiration_time:
            metadata_dict["RetentionExpirationTime"] = blob.retention_expiration_time

        return metadata_dict

    @staticmethod
    def __view_bucket_iam_members(bucket: Bucket):  # type inference on bucket, to make method more protected.
        policy = bucket.get_iam_policy()

        for role in policy:
            members = policy[role]
            print('Role: {}, Members: {}'.format(role, members))

    def __list_blobs_with_prefix(self, bucket: object, prefix, delimiter=None):
        """Lists all the blobs in the bucket that begin with the prefix.

        This can be used to list all blobs in a "folder", e.g. "public/".

        The delimiter argument can be used to restrict the results to only the
        "files" in the given "folder". Without the delimiter, the entire tree under
        the prefix is returned. For example, given these blobs:

            /a/1.txt
            /a/b/2.txt

        If you just specify prefix = '/a', you'll get back:

            /a/1.txt
            /a/b/2.txt

        However, if you specify prefix='/a' and delimiter='/', you'll get back:

            /a/1.txt
        """
        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = self.__storage_client.list_blobs(bucket, prefix=prefix,
                                                 delimiter=delimiter)

        print('Blobs:')
        for blob in blobs:
            print(blob.name)

        if delimiter:
            print('Prefixes:')
            for prefix in blobs.prefixes:
                print(prefix)

    def __check_bucket_exists(self, bucketName: str):
        all_buckets = self.__get_buckets()
        for bucket in all_buckets:
            if bucket.name == bucketName:
                return True
        return False

    def __return_bucket_obj_by_name(self, bucket_name: str):
        """Returns the bucket object - assuming it exists"""
        all_buckets = [(b.id, b) for b in self.__get_buckets()]
        for x in all_buckets:
            if x[0] == bucket_name:
                return x[1]
        return None

    def __recursive_folder_upload(self, path_to_folder, bucket: object):
        """If we choose to upload a folder then there might be other folders nested as such we need to recursively
        upload each one. """
        for filename in os.listdir(path_to_folder):
            if os.path.isdir(os.path.join(path_to_folder, filename)):
                self.__recursive_folder_upload(os.path.join(path_to_folder, filename), bucket)
            else:
                filepath = os.path.join(path_to_folder, filename)
                upload_name = filepath.replace(self.__prj_root_dir, "")
                self.__upload_blob(bucket, filepath, upload_name)
