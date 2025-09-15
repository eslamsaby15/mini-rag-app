from .BaseController import BaseModelController
from .projectController import ProjectController
from models import RespnseSignal
import os 
import re
from fastapi import UploadFile
from fastapi.responses import JSONResponse



class DataController(BaseModelController) :
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    async def Is_Valid_File(self, file :UploadFile) : 
        if file.content_type not in self.app.FILE_ALLOW_TYPES : 
            return False , RespnseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app.FILE_MAX_SIZE * self.size_scale : 
            return False , RespnseSignal.FILE_SIZE_EXCEEDED.value
        
        return True , RespnseSignal.FILE_UPLOAD_SUCCESS.value
    
    def clean_dir_path(self, orginal_path : str) :
        orginal_path = re.sub(r'[^\w.]', '', orginal_path.strip())
        cleanpath  = orginal_path.replace(' ',"_")

        return cleanpath
    
    def generate_random_name(self , orgignal_file : str, project_id : str):
        random_key = self.generate_random_key(length= 10) 

        project_path= ProjectController().get_project_path(file_id=project_id)

        clean_path =self.clean_dir_path(orginal_path= orgignal_file)
        new_file_path = os.path.join(project_path , 
                                random_key + "_" +clean_path)
        
        while os.path.exists(new_file_path) :
            random_key = self.generate_random_key(length= 10) 
            new_file_path = os.path.join(project_path , 
                                    random_key + "_" +clean_path) 
            
        return new_file_path , random_key + "_" +clean_path , clean_path



    