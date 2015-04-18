var host = "python"
var port = "12345"
var 


conn = new Mongo(host+":"+port);
db = conn.getDB("test");
print(db.getCollectionNames());
db = db.getSiblingDB("testData");
print(db.getCollectionNames());

//show collections;