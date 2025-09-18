import os
from helpers import Setting ,app_setting
import random
import string

class BaseModelController:
    def __init__(self):
        self.app = app_setting()

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.project_files = os.path.join(
            self.base_dir , 
            'assets/files'
        )

        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )

        
    def generate_random_key(self , length = 12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits , k = length))
    

    def get_database_path(self , db_name : str) :

        database_path = os.path.join(self.database_dir , 
                                     database_path)
        
        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path