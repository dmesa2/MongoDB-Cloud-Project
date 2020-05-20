import pymongo
from pymongo import MongoClient
import numpy as np
import datetime
from datetime import datetime

cluster = MongoClient("Insert IP Address Here",27017)

db = cluster["Freeway"]

print('--------------------------------------------------------------------------------------------------------')
print("Query #1")
# Count High Speeds: Find the number of speeds > 100 in the data set
speed = db.FreewayLoop.find({"speed": { "$gt": 100}})

count = 0
for s in speed:
    count += 1

print("Number of speeds > 100: ", count)
print()
print('--------------------------------------------------------------------------------------------------------')
print("Query #2")
# Volume: Find the total volume for the station Foster NB for Sept 21, 2011
# Detector IDs for Foster NB: 1361, 1362, 1363

start = datetime(2011, 9, 21, 0, 0, 0)
end = datetime(2011, 9, 21, 23, 59, 59)
agr = [{ '$match': 
        {'$and': [
            {'starttime': {"$gte": start}},
            {'starttime': {"$lte": end}},
            { 'detectorid': { "$gte": 1361 } }, 
            { 'detectorid': { "$lte": 1363 } }]}}, 
        { '$group': {'_id': 1, 'Total': { '$sum': "$volume" } }}]

total_volume = list(db.FreewayLoop.aggregate(agr))

print('The total volume for the station Foster NB for Sept 21, 2011 is: {}'.format(total_volume[0]['Total']))

print()
print('--------------------------------------------------------------------------------------------------------')
print("Query #3")
# Find the average travel time for 7-9am and 4-6pm on Sept 22, 2011 for station Foster NB. Report travel time in seconds
# Detector IDs for Foster NB: 1361, 1362, 1363

start_seven = datetime(2011, 9, 21, 7, 0, 0)
end_nine = datetime(2011, 9, 21, 9, 0, 0)

start_four = datetime(2011, 9, 21, 16, 0, 0)
end_six = datetime(2011, 9, 21, 18, 0, 0)

SevenToNine = db.FreewayLoop.find({'starttime': {'$gte': start_seven, '$lte': end_nine}})
FourToSix = db.FreewayLoop.find({'starttime': {'$gte': start_four, '$lte': end_six}})

SevenToNineNB = []
FourToSixNB = []
for i in SevenToNine:
    if i['detectorid'] >= 1361 and i['detectorid'] <= 1363:
        time_sn = i['starttime'].strftime("%H-%M-%S")
        pt = datetime.strptime(time_sn,'%H-%M-%S')
        total_seconds = pt.second + pt.minute*60 + pt.hour*3600
        SevenToNineNB.append(total_seconds)

for j in FourToSix:
    if j['detectorid'] >= 1361 and j['detectorid'] <= 1363:
        time_fs = j['starttime'].strftime("%H-%M-%S")
        pt = datetime.strptime(time_fs,'%H-%M-%S')
        total_seconds = pt.second + pt.minute*60 + pt.hour*3600
        FourToSixNB.append(total_seconds)

avg_SevenToNine = np.average(SevenToNineNB)
avg_FourToSix = np.average(FourToSixNB)

print("The average travel time for station Foster NB on Sept 22, 2011 between 7-9am is: ", avg_SevenToNine, ' seconds')
print()
print("The average travel time for station Foster NB on Sept 22, 2011 between 4-6pm is: ", avg_FourToSix, ' seconds')
print()

