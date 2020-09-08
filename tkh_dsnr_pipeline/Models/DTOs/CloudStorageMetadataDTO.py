class CloudStorageMetadataDTO(object):
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename') if 'filename' in kwargs else ""
        self.bucketname = kwargs.get('bucketname') if 'bucketname' in kwargs else ""
        self.generationKey = kwargs.get('generationKey') if 'generationKey' in kwargs else ""
        self.upload_date_time = kwargs.get('uploadDateTime') if 'uploadDateTime' in kwargs else ""
