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

        
    def generate_random_key(self , length = 12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits , k = length))
        