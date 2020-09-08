import tkh_dsnr_pipeline.main as pipe

# demonstrate that our program works

#pipe.upload_to_cloud(abs_path_to_file="D:\\swdev\\Repo\\msdt2019\\team1920-datastorage\\Data\\Test Files\\test3.txt")

#pipe.show_files_in_cloud_directory()

#pipe.upload_to_local_storage(source_path="D:\\swdev\\Repo\\msdt2019\\team1920-datastorage\\Data\\Test Files\\",
#                             destination_path="D:\\swdev\\Repo\\msdt2019\\team1920-datastorage\\Data\\Test Files",
#                            compression=True, intended_stored_file_name="test_file_archived")

pipe.upload_to_cloud(abs_path_to_file="D:\\swdev\\Repo\\msdt2019\\team1920-datastorage\\Data\\Test Files\\test2.txt",
                     bucket_name="bramswhatever")
