from helpers import Setting , app_setting

class DataBaseModel:
    def __init__(self, db_client):
        self.db_client = db_client
        self.app_setting = app_setting()