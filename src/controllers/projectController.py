from .BaseController import BaseModelController
import os 


class ProjectController(BaseModelController) : 
    def __init__(self  ):
        super().__init__()

    def get_project_path(self , file_id :str) :
        project_dir = os.path.join(self.project_files , 
                                file_id)
        if not os.path.exists(project_dir) : 
            os.makedirs(project_dir)

        return project_dir