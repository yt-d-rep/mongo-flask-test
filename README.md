# mongo-flask-test

* POST /users
* GET /users/{id}

のみ実装したテスト用ユーザAPI
## Testing


### MongoDB

* システム管理ユーザ: root
* 自動で作成されるアプリ用ユーザ: local

```
$ docker compose up -d
$ mongosh -u root -p root
app> rs.initiate({
    _id: "rs0",
    members: [
        {_id: 0, host: "mongo-primary:27017", priority: 3},
        {_id: 1, host: "mongo-secondary:27017", priority: 2},
        {_id: 2, host: "mongo-tertiary:27017", priority: 1},
        {_id: 3, host: "mongo-arbiter:27017", arbiterOnly: true},
    ],
})
```

### API

```
$ python -m venv .venv
$ . .venv/bin/activate
$ FLASK_APP=app DB_HOST=mongo-primary DB_DATABASE=app DB_PORT=27017 DB_USER_NAME=local DB_PASSWORD=local DB_REPLICASET=rs0 STAGE=local flask run --port=8181 --host=0.0.0.0
```