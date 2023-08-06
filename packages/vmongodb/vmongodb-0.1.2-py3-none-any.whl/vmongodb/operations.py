# basic database operations - decouples from our system all database operations
# inspirado em: W3SCHOOLS - https://www.w3schools.com/python/python_mongodb_create_collection.asp
#               MONGO OFICIAL - http://api.mongodb.com/python/current/tutorial.html
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, InsertManyResult
from bson.objectid import ObjectId

from typing import List, Tuple, Dict, Any


# ----------------- pure operations based on pyMongo API -------------



# MONGO CLIENT -------------------------------------------------------

def _getMongoClient(uri) -> MongoClient:
    return MongoClient(uri)


# MONGO DATABASES -------------------------------------------------------

# if it do not exists it will be created (lazily)
def _getDataBase(client:MongoClient, dbname:str) -> Database:
    return client[dbname]

def _listDataBaseNames(client: MongoClient) -> List[str]:
    return client.list_database_names()

def _doesDataBaseExists(client: MongoClient, dbname:str) -> bool:
    names = _listDataBaseNames(client)
    if dbname in names:
        return True
    else:
        return False



# MONGO COLLECTIONS  -------------------------------------------------------

# if it do not exists it will be created (lazily)
def _getCollection(dbObject: Database, collection_name:str) -> Collection:
    return dbObject[collection_name]

def _listCollectionsNames(dbObject: Database) -> List[str]:
    return dbObject.list_collection_names()


# MONGO DOCUMENTS  -------------------------------------------------------

# The insert_one() method returns a InsertOneResult object, which has a property, inserted_id,
# that holds the id of the inserted document.
def _insert_one(collection: Collection, dict_: Dict[Any, Any]) -> InsertOneResult:
    return collection.insert_one(dict_)

# The returned object contem an attribute with a List of ids_ inserted
def _insert_many(collection: Collection, list_: List[Any]) -> InsertManyResult:
    return collection.insert_many(list_)


# Querying


def _getFirstDocument(c: Collection) -> Cursor:
    return c.find_one()

def _getAllDocuments(c: Collection) -> Cursor:
    return c.find()

def _find_one(c: Collection, filter:Dict[Any, Any]) -> Cursor:
    return c.find_one(filter)


def _find(c: Collection, filter: Dict[Any, Any]) -> Cursor:
    return c.find(filter)


# Couting

def _count_documents(c: Collection, filter:Dict[Any, Any]={}) -> int:
    return c.count_documents(filter)

# Sorting

# Deleting

# Updating


# MONGO ObjectId  -------------------------------------------------------

def _makeObjectId(id_:str) -> ObjectId:
    return ObjectId(id_)



