from fastapi import APIRouter , Depends ,UploadFile ,status ,Request
from helpers import app_setting , Setting
from fastapi.responses import JSONResponse
from controllers import DataController ,ProcessData
from models.Enums.RespnseEnum import RespnseSignal
from .schemes import DataRequest
import aiofiles
import logging
from models.ProjectModel import ProjectModel
from models.AssetModel import AssetsModel
from models.ChunkModel import ChunkModel
from models.db_schema import AssetsSchema ,ChunkSchema
from models.Enums.AssetEnum import AssetTypeEnum
import os 

logger = logging.getLogger('uvicorn.error')
data_router =APIRouter(prefix ='/api/v1/data' ,
                       tags= ['data'])


@data_router.post('/upload/{project_id}') 
async def upload_file(request : Request , project_id : str , file : UploadFile  , 
                app : Setting = Depends(app_setting)) :

    project_model =await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_or_create(project_id= project_id)

    data_controller = DataController()
    is_valid ,signal = await data_controller.Is_Valid_File(file=file)

    if not is_valid :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST , 
            content = {'signal' : signal }
        )
    new_file_path , file_id , orginal_path = data_controller.generate_random_name(orgignal_file=file.filename ,
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
    Assetmodel = await AssetsModel.create_instance(db_client=request.app.db_client)

    asset_resources = AssetsSchema(
        asset_name= file_id ,
        asset_project_id= project.id , 
        asset_type= AssetTypeEnum.FILE.value, 
         asset_size=os.path.getsize(new_file_path)
    )

    asset_record = await Assetmodel.create_AssetModel(assets=asset_resources)


    return JSONResponse ({
        "Project_id": project_id,
        "filename": file.filename,
        'dir' : data_controller.project_files , 
        'valid' : is_valid , 
         'Signal' : signal,
          "orginal_path" : orginal_path , "random_path" : file_id,
         "file_path" :new_file_path , 
        
    })


    
@data_router.post('/prodess/{project_id}')
async def Proces_file(request : Request  , project_id :str , process_request : DataRequest ) : 
    
    
    chunk_size = process_request.chunk_size
    chunk_overlap= process_request.chunk_overlap
    do_reset= process_request.do_reset


    # access DB 
    project_model =await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_or_create(project_id= project_id)
    Assetmodel = await AssetsModel.create_instance(db_client=request.app.db_client)


    project_files_ids = {}
    if process_request.file_id:
        asset_record = await Assetmodel.get_assets_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": RespnseSignal.FILE_ID_ERROR.value,
                }
            )

        project_files_ids = {
            asset_record.id: asset_record.asset_name
        }
    
    else:
        project_files = await Assetmodel.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value,
        )

        project_files_ids = {
            record.id: record.asset_name
            for record in project_files
        }

    if len(project_files_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": RespnseSignal.NO_FILES_ERROR.value,
            }
        )
    
    chunk_model = await ChunkModel.create_instance(
                        db_client=request.app.db_client
                    )
    if do_reset == 1:
            _ = await chunk_model.delete_chunks_by_project_id(
                project_id=project.id
            )
    
    processor = ProcessData(project_id=project_id)
    no_records = 0
    no_files = 0

    for asset_id, file_id in project_files_ids.items():
        file_content = processor.get_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            

        chunks = processor.Process_file_content(file_content=file_content , 
                                                    chunk_size=chunk_size,
                                                    overlap_size= chunk_overlap 
                                                    )
            
        if len(chunks) ==0 or chunks is None :
            return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST ,
                            content = {'signal' : RespnseSignal.PROCESS_CHUNK_FAILED})
        
        
        file_chunks_records = [
            ChunkSchema(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(chunks)
        ]



        no_records += await chunk_model.insert_chunks(file_chunks_records)
        no_files += 1



    return JSONResponse(
        content={
            "signal": RespnseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )