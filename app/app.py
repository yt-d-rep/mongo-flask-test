from flask import Flask, request
from flask_restplus import Api, Resource, abort

from app.resources.models import UserModel, PostModel
from app.modules.json_encorder import CustomJsonEncorder
from app.modules.mongo_client import db_connection
from app.models.user import UserCreate, UserUpdate
from app.models.post import PostCreate
from app.repositories.user import UserRepository
from app.repositories.post import PostRepository

app = Flask(__name__)
api = Api(app)
app.config["RESTPLUS_JSON"] = {"cls": CustomJsonEncorder}

user_model = UserModel(api)
post_model = PostModel(api)



@api.route("/users")
class Users(Resource):
    @db_connection()
    @api.expect(user_model.request_post_model())
    @api.marshal_with(user_model.response_get_model())
    def post(self, db_session):
        """
        ユーザ登録
        """
        request_body = request.get_json(force=True)
        name = request_body.get("name")
        age = request_body.get("age")
        location = request_body.get("location")

        # 登録ドキュメント
        user = UserCreate(
            name=name,
            age=age,
            location=location,
        )
        # 登録
        result = UserRepository.create(db_session, user)

        return result.dict(), 200

@api.route("/users/<string:id>")
class UsersWithId(Resource):
    @db_connection()
    @api.marshal_with(user_model.response_get_model())
    def get(self, id, db_session):
        """
        ユーザ情報取得
        """
        result = UserRepository.get(db_session, id)
        print(result.dict())

        return result.dict(), 200


    @db_connection()
    @api.expect(user_model.request_post_model())
    @api.marshal_with(user_model.response_get_model())
    def put(self, id, db_session):
        """
        ユーザ情報更新
        """
        request_body = request.get_json(force=True)
        name = request_body.get("name")
        age = request_body.get("age")

        # 既存ドキュメント確認
        doc = UserRepository.get(db_session, id)
        if not doc:
            abort(404)

        # 登録ドキュメント
        user = UserUpdate(
            id=id,
            name=name,
            age=age,
        )
        # 登録
        result = UserRepository.update(db_session, id, user)

        return result.dict(), 200

@api.route("/users/nearbyusers")
class UsersNearbyusers(Resource):
    @db_connection()
    @api.param("lat", description="緯度", type=float, required=True)
    @api.param("lng", description="経度", type=float, required=True)
    @api.param("maxDistance", description="最大距離", type=int, default=1000, required=False)
    @api.marshal_with(user_model.response_get_model(), as_list=True)
    def get(self, db_session):
        """
        近くのユーザ情報取得
        """
        params = request.args
        lat = params.get("lat", type=float)
        lng = params.get("lng", type=float)
        max_distance = params.get("maxDistance", type=int)

        results = UserRepository.get_nearbyusers(db_session, lat, lng, max_distance)

        return [result.dict() for result in results], 200

@api.route("/users/<string:user_id>/posts")
class UsersPosts(Resource):
    @db_connection()
    @api.marshal_with(user_model.response_get_with_posts_model())
    def get(self, user_id, db_session):
        """
        ユーザと投稿情報取得
        """
        result = UserRepository.get_with_posts(db_session, user_id)

        return result.dict(), 200

    @db_connection()
    @api.expect(post_model.request_post_model())
    @api.marshal_with(post_model.response_post_model())
    def post(self, user_id, db_session):
        """
        投稿登録
        """
        request_body = request.get_json(force=True)
        title = request_body.get("title")
        message = request_body.get("message")

        # 登録ドキュメント
        post = PostCreate(
            title=title,
            message=message,
            userId=user_id
        )
        # 登録
        result = PostRepository.create(db_session, post)

        return result.dict(), 200




if __name__ == "__main__":
    app.run(debug=True, port=8181, host="0.0.0.0")