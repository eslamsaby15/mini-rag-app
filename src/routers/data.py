from fastapi import APIRouter , Depends ,UploadFile ,status 
from helpers import app_setting , Setting
from fastapi.responses import JSONResponse
from controllers import DataController ,ProcessData
from models.Enums.RespnseEnum import RespnseSignal
from .schemes import DataRequest
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')
data_router =APIRouter(prefix ='/api/v1/data' ,
                       tags= ['data'])


@data_router.post('/upload/{project_id}') 
async def upload_file(project_id : str , file : UploadFile  , 
                app : Setting = Depends(app_setting)) : 
    
    data_controller = DataController()

    is_valid ,signal = await data_controller.Is_Valid_File(file=file)

    if not is_valid :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST , 
            content = {'signal' : signal }
        )
    new_file_path , random_path , orginal_path = data_controller.generate_random_name(orgignal_file=file.filename ,
                                                                                    project_id= project_id)
    

    try : 
         async with aiofiles.open(new_file_path , 'wb') as f : 
            while chunk := await file.read(app.FILE_DEFAULT_CHUNK_SIZE) :
                await f.write(chunk)
    except Exception as e :
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST ,
            content = {'signal' : RespnseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse ({
        "Project_id": project_id,
        "filename": file.filename,
        'dir' : data_controller.project_files , 
        'valid' : is_valid , 
         'Signal' : signal,
          "orginal_path" : orginal_path , "random_path" : random_path,
         "new_file_path" :new_file_path , 
        
    })


    
@data_router.post('/prodess/{project_id}')
async def Proces_file(project_id :str , process_request : DataRequest , 
                      app : Setting = Depends(app_setting)) : 
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap= process_request.chunk_overlap
    do_reset= process_request.do_reset

    processor = ProcessData(project_id=project_id)
    
    file_content = processor.get_content(file_id=file_id)

    chunks = processor.Process_file_content(file_content=file_content , 
                                            chunk_size=chunk_size,
                                            overlap_size= chunk_overlap 
                                            )
    
    if len(chunks) ==0 or chunks is None :
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST ,
                            content = {'signal' : RespnseSignal.PROCESS_CHUNK_FAILED})
    
    return len(chunks)