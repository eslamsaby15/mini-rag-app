from .db_schema import AssetsSchema
from .DataBaseModel import DataBaseModel
from .Enums.DataBaseEnums import DataBaseENUM
from bson.objectid import ObjectId

class AssetsModel(DataBaseModel) :
    def __init__(self, db_client):
        super().__init__(db_client)
        self.connention = self.db_client[DataBaseENUM.COLLECTION_ASSETS_NAME.value]

        
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseENUM.COLLECTION_ASSETS_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseENUM.COLLECTION_ASSETS_NAME.value]
            indexes = AssetsSchema.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_AssetModel(self ,assets : AssetsSchema) :
        result = await self.connention.insert_one(assets.dict(by_alias=True , exclude_unset=True))
        assets.id = result.inserted_id
        return assets
    
    async def get_assets_record(self , asset_project_id: str, asset_name: str) :

        record = await self.connention.find_one({"asset_project_id": ObjectId(asset_project_id) if 
               isinstance(asset_project_id, str) else asset_project_id, "asset_name": asset_name})
        
        if record : 
            return AssetsSchema(**record)
        
        return None
    
    async def get_all_records(self, asset_project_id :str , asset_type :str ) :
        records = await self.connention.find({"asset_project_id" : ObjectId(asset_project_id) 
                                           if isinstance(asset_project_id ,str) 
                                            else asset_project_id ,
                                            'asset_type' : asset_type }).to_list(length =None )
        
        return [
            AssetsSchema(**record)
            for record in records
        ]