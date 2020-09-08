class LocalStorageMetadataDTO(object):
    def __init__(self, **kwargs):
        self.source_path = kwargs.get('source_path') if 'source_path' in kwargs else ""
        self.destination_path = kwargs.get('destination_path') if 'destination_path' in kwargs else ""
        self.upload_date_time = kwargs.get('uploadDateTime') if 'uploadDateTime' in kwargs else ""
        self.compressed = kwargs.get('compressed') if 'compressed' in kwargs else None
        self.intended_stored_file_name = kwargs.get('intended_stored_file_name') if 'intended_stored_file_name' in \
                                                                                    kwargs else ""
