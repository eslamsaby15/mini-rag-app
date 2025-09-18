from ..LLMEnums import LLMEnums , CoHereEnums ,DocumentTypeEnum
from ..LLMinterFace import LLMInterFace 

import cohere
from typing import List, Union

import logging 

class CoHereProvider(LLMInterFace):
    def __init__(self , api_key : str , 
                 default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        self.api_key = api_key
        self.default_input_max_characters= default_input_max_characters
        self.default_generation_max_output_tokens= default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.gen_model_id= None
        self.embedd_model_id = None
        self.embedding_size = None
        self.client= cohere.Client(
            api_key =self.api_key
        )

        self.logger = logging.getLogger(__name__)
    
    def set_embedded_model(self, model_id, embedding_size):
        self.embedd_model_id = model_id 
        self.embedding_size = embedding_size

    def set_generation_model(self, model_id):
        self.gen_model_id =model_id

    def process_text(self, text) :  
        return text[:self.default_input_max_characters].strip()
    
    def construct_prompt(self, prompt : str, role : str): 
        return {'role' : role , 
                'content'  : self.process_text(prompt)}
    

    def embedd_text(self, text  : Union[str, List[str]], document_type = None):

        if not self.embedd_model_id : 
            self.logger.error("Embedding model for CoHere was not set")
            return None
        if not self.client : 
            self.logger.error("CoHere client was not set")
            return None
        
        if isinstance(text, str):
            text = [text]

        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnum.QUERY:
            input_type =CoHereEnums.QUERY

        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [ self.process_text(t) for t in text ],
            input_type = input_type,
            embedding_types=['float'],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None
        
        return [ f for f in response.embeddings.float ]
    

    def generate_text(self, prompt, chat_history = [] ,max_output_tokens = None, temperature = 0.3):
        if not self.client : 
            self.logger("CoHere client was not set")
            return None
        if not self.gen_model_id :
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None
        
        return response.text