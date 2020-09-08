import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from ...Models.Converters.JSONConverter import serialize_object_to_json, deserialize_json_to_object
from ...Models.Converters.compression import compress, decompress
from ...Models.DTOs.LocalStorageMetadataDTO import LocalStorageMetadataDTO
from ...Models.Interfaces.IStorageClientWrapper import IStorageClientWrapper


class LocalStorageClientWrapper(IStorageClientWrapper):

    def __init__(self, prj_root_dir):
        self.__prj_root_dir = prj_root_dir

    def download_from_storage_client(self, **kwargs):
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
        json_parameter_file_path = kwargs.get("srs_path", None)

        source_path = None

        if json_parameter_file_path is not None:
            # download from json file
            with open(str(json_parameter_file_path), 'r') as fp:
                json_model: LocalStorageMetadataDTO = deserialize_json_to_object(fp)  # read in the json file
                fp.close()

            source_path = json_model.source_path

        elif 'source_path' in kwargs:
            source_path = kwargs.get('source_path')
        else:
            raise ValueError("Must provide the \'source_path\' parameter for local storage client to find the file!")

        destination_path = kwargs.get('destination_path', None)
        decompression = kwargs.get('decompression', None)

        if not destination_path:
            destination = self.__prj_root_dir
            print("User did not specify a destination path for the Local storage client to store at,"
                  " using default value {}", self.__prj_root_dir)

        self.__check_dir(destination)

        if decompression:
            print("Decompression mode = True, decompressing archive file.")
            decompress(source_path, destination)
            print("Decompressed file stored in: {}", destination)

        else:
            print("Decompression mode = False, moving archive file.")
            source_parent = str(Path(source_path).parents[0])
            if not (source_parent == destination):
                shutil.move(source_path, destination)
            print("Decompressed file stored in: {}", destination)

    def upload_to_storage_client(self, **kwargs):
        """
                    Store a file/folder to a desired directory in the local storage
                    :param source_path: current directory of the file
                    :param destination_path: destination directory where the file/folder should be moved to
                    :param kwargs:
                        optional - compression (bool): if compression is true, the file/folder will be compressed before saving
                        optional - intended_stored_file_name: the name you want to give the compressed file/folder,
                                         if not given a default name will be given
        """
        if 'source_path' in kwargs:
            source_path = kwargs.get('source_path')
        else:
            raise ValueError("Must provide the \'source_path\' parameter for local storage client to find the file!")

        if 'destination_path' in kwargs:
            destination_path = kwargs.get('destination_path')
        else:
            raise ValueError(
                "Must provide the \'destination_path\' parameter for local storage client to find the destination!")

        compression = kwargs.get('compression')
        intended_stored_file_name = kwargs.get('intended_stored_file_name', None)

        if not os.path.isdir(source_path) and compression:
            raise ValueError("Only directories can be zipped. Single files cannot be zipped.")

        self.__check_dir(destination_path)

        upload_parameters = {'source_path': source_path, 'compression': compression,
                             'destination_path': destination_path}

        if compression:
            # TODO
            # if no name is supplied, name of the zipfile will be the destination; currently funky at move() due to source =/= location
            if not intended_stored_file_name:
                file_name = os.path.split(source_path)[-1]
                intended_stored_file_name = 'archive_' + file_name + "_" + datetime.now().strftime("%A_%d_%B_%Y_%I_%M%p")
                upload_parameters['intended_stored_file_name'] = intended_stored_file_name

            # compression can only happen on DIRECTORIES, and not on single files
            # compress2 takes a name from the kwargs, and source from parameter of save_local
            compress(intended_stored_file_name, source_path)

            # TODO: Perhaps zipfile dumping location can be found by getting a parent/ child from source

            # To find where compress2 dumps zipfile, currently: working directory path
            location = self.__prj_root_dir + "\\" + intended_stored_file_name + ".zip"
            shutil.move(location, destination_path)

            upload_parameters['intended_stored_file_name'] = intended_stored_file_name
            upload_parameters['upload_date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.generate_json_upload_parameters(**upload_parameters)
        else:
            upload_parameters['intended_stored_file_name'] = intended_stored_file_name
            upload_parameters['upload_date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            shutil.move(source_path, destination_path)
            self.generate_json_upload_parameters(**upload_parameters)

    def show_files_stored_by_storage_client(self):
        raise NotImplementedError("Unavailable as of this moment!")

    def delete_file_managed_by_storage_client(self, **kwargs):
        if 'target_path' in kwargs:
            target_path = kwargs.get('target_path')
        else:
            raise ValueError("Must provide the \'target_path\' parameter for local storage client to find the file which is"
                       "to be deleted!")

        if os.path.isdir(target_path):
            logging.warning(
                " You're about to delete a WHOLE directory, are you sure?   \n To be removed:  " + target_path + "\n Type y to continue:")
            remove = input("")
            if remove == "y":
                shutil.rmtree(target_path)
        else:
            os.remove(target_path)

    def generate_json_upload_parameters(self, **kwargs):
        if 'destination_path' in kwargs:
            source_path = kwargs.get('destination_path')
        else:
            raise ValueError("In order to generate retrieval JSON parameter destination_path must be supplied to the "
                       "__generate_json_upload_parameters method!")

        if 'intended_stored_file_name' in kwargs:
            intended_stored_file_name = kwargs.get('intended_stored_file_name')
        else:
            raise ValueError("In order to generate retrieval JSON parameter file, intended_stored_file_name must be supplied"
                       " to the _generate_json_upload_parameters method!")

        timestamp = kwargs.get('upload_date_time')
        compression = kwargs.get('compression')

        metadataModel = LocalStorageMetadataDTO(source_path=source_path,
                                                intended_stored_file_name=intended_stored_file_name,
                                                compressed=compression, upload_date_time=timestamp)

        dir_path = os.path.join(self.__prj_root_dir, "json_files")
        out_name = os.path.split(intended_stored_file_name)[-1].split(".")[0] + ".json"  # the name of the output json file


        if os.path.isdir(dir_path):  # if the folder exists
            with open(os.path.join(dir_path, out_name), 'w') as fp:
                serialize_object_to_json(metadataModel, fp)
                print("Generated retrieval parameters for file {0} in JSON Format. Stored in: {1}",
                      intended_stored_file_name, dir_path)
        else:  # if the folder doesn't exist yet.
            os.makedirs(dir_path)
            with open(os.path.join(dir_path, out_name), 'w') as fp:
                serialize_object_to_json(metadataModel, fp)
                print("Generated retrieval parameters for file {0} in JSON Format. Stored in: {1}",
                      intended_stored_file_name, dir_path)

    # ------ Helper methods ----------

    def __check_dir(self, destination):
        if not os.path.isdir(destination):
            os.mkdir(destination)
