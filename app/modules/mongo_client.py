import os
import pymongo
from functools import wraps


def db_connection():
    """
    Create MongoDB client
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            host = os.getenv("DB_HOST", "127.0.0.1")
            db = os.environ["DB_DATABASE"]
            port = int(os.getenv("DB_PORT", "27017"))
            user = os.environ["DB_USER_NAME"]
            password = os.environ["DB_PASSWORD"]
            rs = os.getenv("DB_REPLICASET", "rs0")

            if os.environ["STAGE"] == "local":
                protocol = "mongodb"
            else:
                protocol = "mongodb+srv"

            client = pymongo.MongoClient(
                f"{protocol}://{user}:{password}@{host}/{db}?replicaSet={rs}&retryWrites=true&w=majority",
                port=port,
            )
            session = None
            try:
                session = client.start_session()
                session.start_transaction()
                response = func(*args, **kwargs, db_session=session)
                session.commit_transaction()
                return response
            except Exception as e:
                if session:
                    session.abort_transaction()
                raise e
            finally:
                if session:
                    session.end_session()
                client.close()

        return wrapper

    return decorator



class DatabaseConstants():
    DB_DATABASE = os.environ["DB_DATABASE"]
    class Collections:
        user = "user"
        post = "post"