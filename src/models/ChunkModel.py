from .db_schema import ChunkSchema
from .DataBaseModel import DataBaseModel
from .Enums.DataBaseEnums import DataBaseENUM
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(DataBaseModel) :
    def __init__(self, db_client):
        super().__init__(db_client)
        
        self.connention = self.db_client[DataBaseENUM.COLLECTION_CHUNKS_NAME.value]
    @classmethod 
    async def create_instance(cls , db_client):
        isinstance = cls(db_client)
        await isinstance.__init__collecton()
        return isinstance


    async def __init__collecton(self): 
        all_collection = await self.db_client.list_collection_names()
        if DataBaseENUM.COLLECTION_CHUNKS_NAME.value not in all_collection  : 
            self.connention = self.db_client[DataBaseENUM.COLLECTION_CHUNKS_NAME.value]
            indexes = ChunkSchema.get_indexes() 
            for index  in  indexes:
                await self.connention.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_chunkdata(self , chunk :ChunkSchema) :
        result = self.connention.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id
        return chunk
    
    async def create_or_get(self , chunk_id : str) :
        record = self.connention.find_one({'_id' :ObjectId(chunk_id)})
        if record is None : 
            return None
        
        return ChunkSchema(**record)
    
    async def insert_chunks(self, chunks: list , batch_size : int = 100 ) :
        for i in range(0,len(chunks) , batch_size) : 
            batch = chunks[i : i+batch_size]
            operations = [ InsertOne(chunk.dict(by_alias=True , exclude_defaults=True))
                 for chunk in batch]
            
            await self.connention.bulk_write(operations)

        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id : ObjectId) :
        result = await self.connention.delete_many({
            'chunk_project_id' :project_id
        })

        return result.deleted_count
    
    async def get_project_cuhnks(self, project_id : ObjectId , 
                                 page_no : int = 1 , page_size : int = 50) : 
        records = await self.connention.find({
                    "chunk_project_id": project_id
                }).skip(
                    (page_no-1) * page_size
                ).limit(page_size).to_list(length=page_size)
        
        return [ChunkSchema(**record) for record in records]