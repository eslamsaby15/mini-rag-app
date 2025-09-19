from fastapi import Request , FastAPI , status , APIRouter
from fastapi.responses import JSONResponse
from models.ProjectModel import ProjectModel 
from models.ChunkModel import ChunkModel
from controllers import NLPController
from .schemes import PushReqScema ,SearchRequest
import logging
from models.Enums.RespnseEnum import RespnseSignal
from fastapi.encoders import jsonable_encoder

nlp_router= APIRouter(prefix='/api/v1/nlp' , 
                      tags=['nlp'])


@nlp_router.post("/index/push/{project_id}")
async def index_project(request : Request , project_id : str , 
                        push_request : PushReqScema ) : 
    
    project_model = await ProjectModel.create_instance(db_client= 
                                                       request.app.db_client)
    project = await project_model.get_or_create(project_id= project_id)

    if not project : 
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST ,
                            content= {'signal' : RespnseSignal.PROjECT_NOT_FOUND.value})
    
    nlp_controller = NLPController(vectordb_client= request.app.vectordb_client ,
                                   embedding_client= request.app.embedding_client ,
                                   generation_client= request.app.generation_client,
                                   template_parser =request.app.template_parser )
    
    chunk_model = await ChunkModel.create_instance(db_client=  request.app.db_client)
    

    has_records= True
    page_no = 1 
    inserted_count = 0 
    idx = 0
    while has_records :
        page_chunks = await  chunk_model.get_project_cuhnks(project_id= project.id , page_no= page_no)
        if len(page_chunks):
            page_no += 1

        if not page_chunks or len(page_chunks) == 0 : 
            has_records =False 

        chunk_ids = list(range (idx,idx + len(page_chunks)))

        is_inserted = nlp_controller.index_into_vector_db(project=project ,
                                                chunks= page_chunks , 
                                                do_reset= push_request.do_reset,
                                                chunks_ids= chunk_ids)
        
        if not is_inserted : 
            return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST ,
                            content= {'signal' : RespnseSignal.INSERT_VECTOR_DB_ERROR.value})

        inserted_count += 1 
        
    return JSONResponse(
        content={'signal' : RespnseSignal.INSERT_VECTOR_DB_SUCESS.value ,
                 'count': inserted_count}
    )
        



@nlp_router.get("/index/getinfo/{project_id}")
async def get_info_project(request : Request , project_id : str , 
                        ) : 
    
    project_model = await ProjectModel.create_instance(db_client= 
                                                       request.app.db_client)
    project = await project_model.get_or_create(project_id= project_id)

    if not project : 
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST ,
                            content= {'signal' : RespnseSignal.PROjECT_NOT_FOUND.value})
    

    nlp_controller = NLPController(vectordb_client= request.app.vectordb_client ,
                                   embedding_client= request.app.embedding_client ,
                                   generation_client= request.app.generation_client,
                                   template_parser= request.app.template_parser)
    
    collection_info = nlp_controller.get_collection_info(project=project)
    
    
   
   
    return JSONResponse( 
            content= {'signal' : RespnseSignal.VECTOR_COLLECTION_RETRIEVED.value,
                        'collection info' : collection_info})
    



@nlp_router.post("/index/search/{project_id}")
async def search_project(request : Request , project_id : str , 
                        search_request : SearchRequest) : 
    
    project_model = await ProjectModel.create_instance(db_client= 
                                                       request.app.db_client)
    project = await project_model.get_or_create(project_id= project_id)

    if not project : 
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST ,
                            content= {'signal' : RespnseSignal.PROjECT_NOT_FOUND.value})
    

    nlp_controller = NLPController(vectordb_client= request.app.vectordb_client ,
                                   embedding_client= request.app.embedding_client ,
                                   generation_client= request.app.generation_client,
                                   template_parser =request.app.template_parser )
    
    results = nlp_controller.search_db_collection(project=project , 
                                                          text = search_request.text ,
                                                           limit= search_request.limit )
    
    
   
    if not results:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": RespnseSignal.VECTORDB_SEARCH_ERROR.value
                }
            )
    
    return JSONResponse(
        content={
            "signal": RespnseSignal.VECTORDB_SEARCH_SUCCESS.value,
            "results": [ result.dict()  for result in results ]
        }
    )



@nlp_router.post("/index/answer/{project_id}")
async def answerQuery(request : Request , project_id : str , 
                        search_request : SearchRequest) : 
    
    project_model = await ProjectModel.create_instance(db_client= 
                                                       request.app.db_client)
    project = await project_model.get_or_create(project_id= project_id)

    if not project : 
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST ,
                            content= {'signal' : RespnseSignal.PROjECT_NOT_FOUND.value})
    

    nlp_controller = NLPController(vectordb_client= request.app.vectordb_client ,
                                   embedding_client= request.app.embedding_client ,
                                   generation_client= request.app.generation_client,
                                   template_parser =request.app.template_parser )
    
    answer, full_prompt, chat_history = nlp_controller.generate_answer(project=project , 
                                                          query = search_request.text ,
                                                           limit= search_request.limit )
    
    if not answer:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": RespnseSignal.RAG_ANSWER_ERROR.value
                }
        )
    
    return JSONResponse(
        content={
            "signal": RespnseSignal.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history
        }
    )