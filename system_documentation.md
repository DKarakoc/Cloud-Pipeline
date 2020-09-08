# System Documentation

This documentation aims to explain the basic layout of the project for future contributors to easily navigate the code.

---

The project __tkh_pipeline__, is a data management pipeline used to easily access and store data files
across different sources. The primary use is as an interface to the google cloud storage API for storing and retrieving files from the google cloud. However, it also supports local storage for moving files across a shared network to different directories. The modular design of the project also aims to allow for easy addition of future clients, such as for example amazons AWS.

The project tries to give the user the ability to upload and download data from inside their project file with a minimal code footprint - ie. in a single line of code. The user would use this project when they want to easily store large machine learning data files to the google cloud so free up space on the local drive, or simply keep a small project directory. Similarly, this also makes it easy to share large files with a collaborator that also has access to the same google cloud client. As such, the project can described as analogous to _git_, only for large data files instead of code.

## Design

The code base is designed to be as modular as possible. This way different cloud clients can be easily added to the existing client handler. The current project only includes a _google cloud client_ which acts as an _adapter_ to the google cloud storage API, and a _local storage client_ which handles moving and compressing files stored on a local network. However, through the use of a sort of decorator pattern, adding new clients - ie. AWS - should require minimal modification to the code.

The code is split up into 3 main aspects: the client interface which connects the different clients and handles authentication, a couple of data storage classes, and a number of utility functions which work mainly with reading and writing JSON files.

#### Interface

The __IStorageClientWrapper__ class acts as a python metaclass, analogous to a java interface/abstract-class. It implements a number of methods that will be overwritten by all clients that are added to the project. These include upload, downloading files; showing the files that are stored in a client; as well as another method for creating JSON files which will be discussed later on.

The _IStorageClientWrapper_ is then implemented by a client class such as for example the __GoogleCloudClientWrapper__, and the __LocalStorageClientWrapper__. The clients then overwrite the methods shown in the _IStorageClientWrapper_ allowing them to upload and download files based on their direct implementation. Similarly, to add additional functionality to each client a method simply needs to be instantiated in the metaclass and then overwritten in the client class.

The __IStorageClientWrapper__ class is also wrapped by the __ClientWrapperHandler__ which acts as a _singleton_ pattern making sure that only a single instance of a client can be created. This helps prevent users from creating unnecessary amounts of clients accessing the same data, as well as preventing any potential issues that may arise from different users accessing the same data simultaneously.

#### GoogleCloudClientWrapper

The google cloud client is currently the only cloud storage client implemented. The class acts as a small _facade_ pattern around the Google Storage client created by google. Authenticating with the google client is done by passing a specific JSON file to a function. This returns a client object which can methods called to work with files.


#### Authentication

When trying to use a cloud client such as the _GoogleCloudClientWrapper_ a Authentication.json file is needed. This file needs to be saved with the exact name - __Authentication.json__ - to the root directory of the users project. When a upload or download method call to a cloud client, such as _GoogleCloudClientWrapper_ is made the client will first look for and read in the authentication file. It does this by calling the __DSNRPConfig__ class when instantiating the client. This class will search for the Authentication file in the project root directory. It will then pass the path of the file to the _GoogleCloudClientWrapper_ which will make an API call returning a valid client which allows the user to access the data. Currently, the project only supports a single Authentication file for a client.

For local storage this authentication file isn't needed, as there is no authentication necessary.



#### JSON files

A fundamental aspect of the project is the creation of JSON files whenever a file is uploaded to a cloud client or moved to some local network directory. The purpose of these files is to keep track of the data files that are part of a project and are being moved. They also make it quite easy to download a specific file. If a user wants to download a specific file they can simply pass the absolute path to the corresponding JSON file to the download method. Similarly, they can only the JSON file to a collaborator to allow them to also download the file - assuming they also have authentication to the cloud client if necessary.

A JSON file is created everytime a file is uploaded through a call to the client specific implementation of _generate_json_upload_parameters()_. This method creates instantiates a class which stores the variables that should be added to the JSON file. The necessary information that should be stored in a JSON file can change depending on the client in use, as such, there is a different class for each client, however, if desired a new client could use an existing class. The current JSON parameter classes are __CloudStorageMetadataDTO__, and __LocalStorageMetadataDTO__.

These classes, once instantiated with the required data are passed to a class __JSONConverter__, which calls another class __Utilities__ which can serialize the _MetadataDTO_ object into a dictionary object which can easily be written to a file and saved as a _.json_ file.

Similarly, when trying to download a data file by passing the path to a JSON file, another method _deserialize_json_to_object_ can take a dictionary, read in from a _.json_ file and deserialize it into the corresponding _MetadataDTO_ class.
