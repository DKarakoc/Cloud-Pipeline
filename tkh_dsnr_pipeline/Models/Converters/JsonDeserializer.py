import json


class JasonDeserializer:

    def __init__(self):
        """
        Init variables as None when class object created
        """
        self.type = None  # string
        self.project_id = None  # string
        self.private_key_id = None  # string
        self.private_key = None  # string
        self.client_email = None  # sting
        self.client_id = None  # string
        self.auth_uri = None  # string - url
        self.token_uri = None  # string - url
        self.auth_provider_cert_url = None  # string - url
        self.client_cert_url = None  # string - url
        self.dict_data = None # dict - json data

    def read_data(self, filePath):
        """
        reads json data from a file and saves the values to the class keys
        :param filePath:
        :return None:
        """
        with open(filePath) as json_file:
            data = json.load(json_file)
            # for k, v in data.items():
            data_list = list(data.items())  # convert dict to list of tuples
            self.dict_data = data
            self.type = data_list[0][1]
            self.project_id = data_list[1][1]
            self.private_key_id = data_list[2][1]
            self.private_key = data_list[3][1]
            self.client_email = data_list[4][1]
            self.client_id = data_list[5][1]
            self.auth_uri = data_list[6][1]
            self.token_uri = data_list[7][1]
            self.auth_provider_cert_url = data_list[8][1]
            self.client_cert_url = data_list[9][1]

    def output_dict(self):
        """Prints the json dictionary"""
        print(json.dumps(self.dict_data, indent=4, sort_keys=False))

    def __str__(self):
        """toString method"""
        return "\n".join([self.type, self.project_id, self.private_key_id, self.private_key,
                          self.client_email, self.client_id, self.auth_uri, self.token_uri,
                          self.auth_provider_cert_url, self.client_cert_url])
