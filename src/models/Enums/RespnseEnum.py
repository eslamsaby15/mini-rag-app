from enum import Enum

class RespnseSignal(Enum) : 
    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESS_CHUNK_SUCCESS = 'response_chunk_success'
    PROCESS_CHUNK_FAILED = 'response_chunk_failed'
    NoFileFound ='NoFileFound' 