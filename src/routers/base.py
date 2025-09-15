from fastapi import Depends, APIRouter 
from fastapi.responses import JSONResponse
from helpers import app_setting , Setting

base_router = APIRouter(prefix = '/api/v1' , 
                       tags = ['welcome'])

@base_router.get('/Welcome')
def Welcome():
    return 'Welcome ya baby'


@base_router.get('/get_info') 
def Info(app_setting : Setting = Depends(app_setting)) : 
    app_name = app_setting.APP_NAME
    app_version = app_setting.APP_VERSION
    app_creator= app_setting.APP_CREATOR


    return JSONResponse(
        {'app.name' : app_name,
         'app.version' : app_version,
         'app.creator' : app_creator}
    )

