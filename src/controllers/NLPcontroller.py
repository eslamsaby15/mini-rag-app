from .BaseController import BaseModelController
from models.db_schema import Project
from models.db_schema import ChunkSchema
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnum
import json

class NLPController(BaseModelController):
    def __init__(self,vectordb_client ,generation_client ,embedding_client):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client =embedding_client


    def create_collection_name(self,project_id) : 
        return f"collection_{project_id}".strip()
    
    def reset_db_schema(self,project:Project) :
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectodb_client.delete_collection(collection_name = collection_name)
    
    def get_collection_info(self,project : Project) :
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name = collection_name)

        
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self , project : Project , chunks : List[ChunkSchema] ,
                                chunks_ids : List[int]  ,
                                do_reset : bool = False) :
        
        collection_name = self.create_collection_name(project_id=project.project_id)

        texts =[ c.chunk_text for c in chunks]
        meta_data= [c.chunk_metadata for c in chunks]

        vectors = [
            self.embedding_client.embedd_text(text  =  text,
                                               document_type = DocumentTypeEnum.DOCUMENT.value)

                                               for text in texts
    
        ]

        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        _ = self.vectordb_client.insert_many(
            collection_name = collection_name ,
            texts = texts , 
            vectors= vectors, metadata= meta_data, 
                          record_ids= chunks_ids 
        )

        return True
    
    def search_db_collection(self, project :Project, text :str , limit : int = 10) : 

        collection_name = self.create_collection_name(project_id=project.project_id)
        
        info = self.get_collection_info(project=project)
        print("Collection info:", info)
        

        
        vector = self.embedding_client.embedd_text(text = text , 
                                                  document_type = DocumentTypeEnum.QUERY.value)

         
        if not vector or len(vector) ==0 : 
            return []
        
        results = self.vectordb_client.search_by_vector(collection_name = collection_name,
                                                        vector =vector ,
                                                        limit = limit)
        
        print("Search results:", results)

        if not results:
            return []

        return results


