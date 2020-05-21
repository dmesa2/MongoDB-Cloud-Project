# This python script will remove the following Keys and Values from each document in Freeway_LoopData
#    - speed : 0
#    - speed: NaN
#    - volume: NaN
#    - occupancy: NaN

import pymongo
from pymongo import MongoClient
import numpy as np

cluster = MongoClient("Insert IP Address Here",27017)

db = cluster["Freeway"]
collection = db["FreewayLoop"]

collection.update_many({"speed": 0}, { "$unset" : {"speed" : 1 }})

collection.update_many({"speed": np.nan}, { "$unset" : {"speed" : 1 }})

collection.update_many({"volume": np.nan}, { "$unset" : {"volume" : 1 }})

collection.update_many({"occupancy": np.nan}, { "$unset" : {"occupancy" : 1 }})


