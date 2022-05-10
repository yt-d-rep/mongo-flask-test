from bson.objectid import ObjectId

from app.models.user import UserCreate, UserRead
from app.modules.mongo_client import DatabaseConstants as DB



class UserRepository:
    @staticmethod
    def get(db_session, id: str) -> UserRead:
        user = db_session.client[DB.DB_DATABASE][DB.Collections.user]\
            .find_one({"_id": ObjectId(id)}, session=db_session) # "_id"べた書きがイケてない
        if not user:
            return {}
        return UserRead(**user).dict()

    @staticmethod
    def create(db_session, entity: UserCreate) -> UserRead:
        d = entity.dict()
        result = db_session.client[DB.DB_DATABASE][DB.Collections.user]\
            .insert_one(d, session=db_session)
        id = str(result.inserted_id)
        return UserRepository.get(db_session, id)