from .db_schema import Project
from .DataBaseModel import DataBaseModel
from .Enums.DataBaseEnums import DataBaseENUM


class ProjectModel(DataBaseModel) :
    def __init__(self, db_client):
        super().__init__(db_client)
        self.connention = self.db_clinet[DataBaseENUM.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project : Project) :
        result = await self.connention.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id = result._id
        return project
    

    async def get_or_create(self ,project_id :str) : 
        record = await self.connention.find_one({'project_id' : project_id})
        if record is None :
            project = Project(project_id=project_id)
            result = self.create_project(project=project)
            return result
        return Project(**record)
    
    async def get_all_project(self , page : int = 1 , page_size : int = 10) :
        total_documents =await self.connention.count_documents({})

        total_pages = total_documents // page_size
        if total_documents % total_pages > 0 :
            total_pages +=1 

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        
        projects = []
        async for doc in cursor : 
            projects.append(
                Project(**doc)
            )

        return projects , total_pages
    
    @classmethod 
    async def create_instance(cls , db_client : object) :
        instance = cls(db_client)
        await instance.__init__collection()
        return instance

    async def __init__collection(self) :
        all_collection =await self.db_clinet.list_collection_names()
        if DataBaseENUM.COLLECTION_PROJECT_NAME.value not in all_collection : 
            self.connention  =self.db_clinet[DataBaseENUM.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes :
                await self.connention.create_index(index["key"],
                    name=index["name"],
                    unique=index["unique"])

   