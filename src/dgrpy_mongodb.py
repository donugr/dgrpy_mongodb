import pymongo
from pymongo import MongoClient
import json

class _mongoOperation:
    def __init__(self,MONGO_DB,MONGO_Collection,MONGO_HOST="localhost",MONGO_PORT=27017):
        self.MONGO_CLIENT = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.MONGO_CLIENT.get_database(MONGO_DB)
        self.collection = self.db[MONGO_Collection]

    def find(self, entity: 'mongoResult') -> 'mongoResult':
        if bool(entity._getShowField()) == True:
            item = self.collection.find(entity._getQuery(), entity._getShowField())
        else:
            item = self.collection.find(entity._getQuery())
            
        res = {
            "status" : "empty",
            "detail": "empty"
        }
        for x in item:
            if "_id" in x:
                res = {
                    "status" : "exist",
                    "detail": x
                }
                break
        return mongoResult(query=entity._getQuery(), result=res)
    
    def findAggregate(self, entity: 'mongoResult') -> 'mongoResult':
        item = self.collection.aggregate(entity._getQuery())
        res = {
            "status" : "empty",
            "detail": "empty"
        }
        xx = []
        for x in item:
            if "_id" in x:
                xx.append(x)
        res = {
            "status" : "empty" if len(xx) == 0 else "exist",
            "detail": xx
        }
        return mongoResult(query=entity._getQuery(), result=res)

    def findAll(self, entity: 'mongoResult') -> 'mongoResult':
        if bool(entity._getShowField()) == True:
            item = self.collection.find(entity._getQuery(), entity._getShowField())
        else:
            item = self.collection.find(entity._getQuery())
        res = {
            "status" : "empty",
            "detail": "empty"
        }
        xx = []
        for x in item:
            if "_id" in x:
                xx.append(x)
        res = {
            "status" : "empty" if len(xx) == 0 else "exist",
            "detail": xx
        }
        return mongoResult(query=entity._getQuery(), result=res)


    def insert(self, entity: 'mongoResult') -> 'mongoResult':        
        try:
            item = self.collection.insert_one(entity._getQuery())
            res = {
                    "status": "ok",
                    "detail": entity._getQuery()
            }
        except pymongo.errors.PyMongoError as e:
            res = {
                    "status": "error",
                    "detail": "not inserted to DB " + str(e)
            }
        return mongoResult(query=entity._getQuery(), result=res)

    def insertMany(self, entity: 'mongoResult') -> 'mongoResult':        
        try:
            item = self.collection.insert_many(entity._getQuery())
            res = {
                    "status": "ok",
                    "detail": entity._getQuery()
            }
        except pymongo.errors.PyMongoError as e:
            res = {
                    "status": "error",
                    "detail": "not inserted to DB " + str(e)
            }
        return mongoResult(query=entity._getQuery(), result=res)

    def delete(self, entity: 'mongoResult') -> 'mongoResult':
        try:
            item = self.collection.delete_many(entity._getQuery())
            res = {
                "status": "ok",
                "detail": entity._getQuery()
            }
        except pymongo.errors.PyMongoError as e:
            res = {
                "status": "error",
                "detail": "Error Delete Channel : " + str(e)
            }
        return mongoResult(query=entity._getQuery(), result=res)

    def update(self, entity: 'mongoResult') -> 'mongoResult':        
        try:
            item = self.collection.update_one(entity._getQuery(), entity._getFilter())
            #det = "Members now can send Comment" if entity._getQuery()["MemberAllowComment"] == "yes" else "Members Comment Disabled by Owner"
            res = {
                "status": "ok",
                "detail": "ok"
            }
        except pymongo.errors.PyMongoError as e:
            res = {
                "status": "error",
                "detail": "Error Update Comments : " + str(e)
            }

        return mongoResult(query=entity._getQuery(), result=res, filter=entity._getFilter())


class mongoResult:
    def __init__(self, query: str, filter: dict = {}, result: dict = {}, data: dict = {}, showfield: dict = {}) -> None:
        self.reqQuery = query if (type(query) is dict) or (type(query) is list) else json.loads(query)  # type: dict
        self.reqResult = result
        self.reqFilter = filter
        self.reqShowField = showfield
        self.reqData = data

    def _getQuery(self):
        return self.reqQuery

    def _getData(self) -> dict:
        return self.reqData

    def _getFilter(self) -> dict:
        return self.reqFilter

    def _getShowField(self) -> dict:
        return self.reqShowField
    
    def _result(self) -> dict:
        resDT = {
            "reqResult" : self.reqResult,
            "reqQuery" : self.reqQuery,
            "reqFilter" : self.reqFilter
        }
        return resDT if (type(resDT) is dict) or (type(resDT) is list) else None

def InsertMongo(mongoOps,InsertQuery):
    insertReq2 = mongoResult(query=InsertQuery)
    insertReq2 = mongoOps.insert(insertReq2)
    resinsertReq2 = insertReq2._result()
    return resinsertReq2


def GetMongoFindOne(mongoOps,findQuery, showField={}):
    
    if bool(showField) == True:
        findMongo = mongoResult(query=findQuery,showfield=showField)
    else:
        findMongo = mongoResult(query=findQuery)
    findMongo = mongoOps.find(findMongo)
    resfindMongo = findMongo._result()
    return resfindMongo


def GetMongoFindAll(mongoOps, findQuery, showField={}):
    if bool(showField) == True:
        findMongo = mongoResult(query=findQuery,showfield=showField)
    else:
        findMongo = mongoResult(query=findQuery)
    findMongo = mongoOps.findAll(findMongo)
    resfindMongo = findMongo._result()
    return resfindMongo
    
def GetMongoFindAggregate(mongoOps, findQuery):
    findMongo = mongoResult(query=findQuery)
    findMongo = mongoOps.findAggregate(findMongo)
    resfindMongo = findMongo._result()
    return resfindMongo
    

def UpdateMongo(mongoOps,findQuery,UpdateFilter):
    #UpdateFilter = {
        #"$set":  UpdateArray
    #}

    updateMongo = mongoResult(query=findQuery, filter=UpdateFilter)
    UpdateMongo = mongoOps.update(updateMongo)
    resUpdateMongo = UpdateMongo._result()
    return resUpdateMongo