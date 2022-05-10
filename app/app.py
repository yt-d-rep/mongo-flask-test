from flask import Flask, request
from flask_restplus import Api, Resource

from app.modules.mongo_client import db_connection
from app.models.user import UserCreate
from app.repositories.user import UserRepository

app = Flask(__name__)
api = Api(app)



@api.route("/users")
class Users(Resource):
    @db_connection()
    def post(self, db_session):
        """
        ユーザ登録
        """
        request_body = request.get_json(force=True)
        name = request_body.get("name")
        age = request_body.get("age")

        # 登録ドキュメント
        user = UserCreate(
            name=name,
            age=age,
        )
        # 登録
        result = UserRepository.create(db_session, user)

        return result, 200



@api.route("/users/<string:id>")
class Users(Resource):
    @db_connection()
    def get(self, id, db_session):
        """
        ユーザ情報取得
        """
        result = UserRepository.get(db_session, id)

        return result, 200



if __name__ == "__main__":
    app.run(debug=True)