from doctest import Example
from flask_restplus import fields



class UserModel:
    id = fields.String(title="id", example="627b0b577c20f68ccd2739f9", description="ID")
    name = fields.String(title="name", example="627b0b577c20f68ccd2739f9", description="名前")
    age = fields.Integer(title="age", example=1, description="年齢")
    coordinates = fields.List(fields.Float(), title="coordinates")

    def __init__(self, api):
        self.api = api

    def request_post_model(self):
        return self.api.model(
            name="User Post Request",
            model={
                self.name.title: self.name,
                self.age.title: self.age,
                "location": fields.Nested(
                    self.api.model(
                        name="Location",
                        model={
                            self.coordinates.title: self.coordinates,
                        },
                    ),
                ),
            }
        )

    def response_get_model(self):
        return self.api.model(
            name="User Get Response",
            model={
                self.id.title: self.id,
                self.name.title: self.name,
                self.age.title: self.age,
                "location": fields.Nested(
                    self.api.model(
                        name="Location",
                        model={
                            self.coordinates.title: self.coordinates,
                        },
                    ),
                ),
            }
        )

    def response_get_with_posts_model(self):
        return self.api.model(
            name="User Get Response",
            model={
                self.id.title: self.id,
                self.name.title: self.name,
                self.age.title: self.age,
                "posts": fields.List(
                    fields.Nested(
                        self.api.model(
                            name="Post Get Response",
                            model={
                                PostModel.id.title: PostModel.id,
                                PostModel.title.title: PostModel.title,
                                PostModel.message.title: PostModel.message,
                            }
                        ),
                        as_list=True
                    )
                )
            }
        )
    


class PostModel:
    id = fields.String(title="id", example="627b0b577c20f68ccd2739f9", description="ID")
    userId = fields.String(title="userId", example="627b0b577c20f68ccd2739f9", description="ユーザID")
    title = fields.String(title="title", example="TITLE", description="タイトル")
    message = fields.String(title="message", example="MESSAGE", description="本文")

    def __init__(self, api):
        self.api = api
        
    def request_post_model(self):
        return self.api.model(
            name="Post Post Request",
            model={
                self.title.title: self.title,
                self.message.title: self.message,
                self.userId.title: self.userId,
            }
        )

    def response_post_model(self):
        return self.api.model(
            name="Post Post Response",
            model={
                self.id.title: self.id,
                self.title.title: self.title,
                self.message.title: self.message,
                self.userId.title: self.userId,
            }
        )