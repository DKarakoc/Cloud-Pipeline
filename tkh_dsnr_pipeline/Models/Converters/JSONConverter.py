import json as JSON
from .. import Utilities


def serialize_object_to_json(obj: object, fp):
    """
    :param obj: a class object storing the metadata of a file
    :param fp: an open file
    :return:
    """
    return JSON.dump(obj, fp, default=Utilities.convertObjectToDict, indent=4, ensure_ascii=True)


def deserialize_json_to_object(json_file: object):
    return JSON.load(json_file, object_hook=Utilities.dict_to_obj)
