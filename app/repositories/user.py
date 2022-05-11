from bson.objectid import ObjectId

from app.models.user import UserCreate, UserRead, UserReadWithPosts
from app.modules.mongo_client import DatabaseConstants as DB



class UserRepository:
    @staticmethod
    def get(db_session, id: str) -> UserRead:
        result = db_session.client[DB.DB_DATABASE][DB.Collections.user]\
            .find_one({"_id": ObjectId(id)}, session=db_session) # "_id"べた書きがイケてない
        if not result:
            return {}
        return UserRead(**result)

    @staticmethod
    def create(db_session, entity: UserCreate) -> UserRead:
        d = entity.dict()
        result = db_session.client[DB.DB_DATABASE][DB.Collections.user]\
            .insert_one(d, session=db_session)
        id = str(result.inserted_id)
        return UserRepository.get(db_session, id)

    @staticmethod
    def get_with_posts(db_session, user_id: str) -> UserReadWithPosts:
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(user_id),
                }
            },
            {
                "$lookup": {
                    "from": DB.Collections.post,
                    "localField": "_id",
                    "foreignField": "userId",
                    "as": "posts",
                }
            }
        ]
        cursor = db_session.client[DB.DB_DATABASE][DB.Collections.user]\
            .aggregate(pipeline)
        result = list(cursor)
        if not result:
            return {}
        return UserReadWithPosts(**result[0])