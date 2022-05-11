from bson.objectid import ObjectId

from app.models.post import PostCreate, PostRead
from app.modules.mongo_client import DatabaseConstants as DB



class PostRepository:
    @staticmethod
    def get(db_session, id: str) -> PostRead:
        result = db_session.client[DB.DB_DATABASE][DB.Collections.post]\
            .find_one({"_id": ObjectId(id)}, session=db_session) # "_id"べた書きがイケてない
        if not result:
            return {}
        return PostRead(**result)

    @staticmethod
    def create(db_session, entity: PostCreate) -> PostRead:
        d = entity.dict()
        result = db_session.client[DB.DB_DATABASE][DB.Collections.post]\
            .insert_one(d, session=db_session)
        id = str(result.inserted_id)
        return PostRepository.get(db_session, id)