from .BaseController import BaseModelController
from .projectController import ProjectController
from langchain_community.document_loaders import PyMuPDFLoader ,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessEnum
import os
class ProcessData(BaseModelController):
    def __init__(self,project_id):
        super().__init__()
        self.project_id = project_id
        self.project_path =ProjectController().get_project_path(file_id=project_id)
                                        

    def get_ext(self , file_id : str) : 
        ext = os.path.splitext(file_id)[-1]
        return ext
    
    def get_file_loder(self, file_id :str) : 
        file_ext = self.get_ext(file_id =file_id)
        file_path = os.path.join(self.project_path , 
                                 file_id)
        
        if file_ext == ProcessEnum.TXT.value :
            loader = TextLoader(file_path , encoding='utf-8')
            return loader
        elif file_ext == ProcessEnum.PDF.value :
            loader = PyMuPDFLoader(file_path )
            return loader
        
        
        return None
    
    def get_content(self, file_id : str) : 
        loader = self.get_file_loder(file_id=file_id)
        return loader.load()
    
    def Process_file_content(self, file_content: list,
                            chunk_size: int=100, overlap_size: int=20) :
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size =chunk_size ,
            chunk_overlap =overlap_size ,
             length_function=len,
        )

        file_content_text = [ rec.page_content  for rec in file_content]
        file_metadatas = [ rec.metadata  for rec in file_content]

        chunks = text_splitter.create_documents(file_content_text ,
                                                 file_metadatas)
        

        return chunks