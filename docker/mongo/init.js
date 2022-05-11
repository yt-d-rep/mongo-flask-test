db.createUser({
    user: "local",
    pwd: "local",
    roles: [
        {role: "readWrite", db: "app"},
    ],
});

db.createCollection("user", {});
db.createCollection("post", {});

// var error = rs.initiate({
//     _id: "rs0",
//     members: [
//         {_id: 0, host: "mongo-primary:27017"},
//         {_id: 1, host: "mongo-secondary:27017"},
//     ],
// })
// printjson(error)