// Create users
db.createUser({
    user: "local",
    pwd: "local",
    roles: [
        {role: "readWrite", db: "app"},
    ],
});

// Create collections
db.createCollection("user", {});
db.createCollection("post", {});

// Create Indexes
db.user.createIndex({"location": "2d"});

db.user.find({location: {$near: [139.684011, 35.740095], $minDistance: 0, $maxDistance: 10}})

db.places.insertMany([
    {
        "name": "Tokyo Station",
        "location": {
            "type": "Point",
            "coordinates": [139.76732, 35.681246]
        }
    },
    {
        "name": "Ikebukuro Station",
        "location": {
            "type": "Point",
            "coordinates": [139.711214, 35.729888]
        }
    },
])