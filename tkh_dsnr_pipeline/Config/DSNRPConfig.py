import os
import sys


class DSNRPConfig:

    def __init__(self, prj_root_dir: str):
        # self.GoogleCloudAPIKeyDir = os.path.dirname(
        #     os.path.realpath( __file__ ) ) + '\\orbital-citizen-113115-eab3d0b6c3d5.json'

        self.prj_root_dir = prj_root_dir
        self.GoogleCloudAPIKeyFile = self.search_auth()

        self.SRSStorageDir = os.getcwd() + '/tkh_dsnr_pipeline Storage Retrieval Scripts'

    # TODO: search for the authentication file in the root of the project folder [ not this projects folder ]
    def search_auth(self):
        for filename in os.listdir( self.prj_root_dir ):
            if filename == "Authentication.json":
                return self.prj_root_dir + "/Authentication.json"
        raise BaseException( "No Authentication.json file found.\n"
                             "There needs to be a file named Authentication.json in the root directory of your project" )

    def getGoogleCloudAPIKeyDir(self):
        return self.GoogleCloudAPIKeyFile
