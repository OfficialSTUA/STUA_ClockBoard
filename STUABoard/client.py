

import aiohttp, asyncio, time
from functools import partial
from numpy import mask_indices
import requests, csv, datetime, math, os, json, calendar
import time as te
from abc import ABC, abstractmethod
from xml.etree.ElementTree import fromstring, ElementTree as ET
import gtfs_realtime_pb2, nyct_subway_pb2, stua, dotenv

dotenv.load_dotenv()

stua.keyMTA(os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

t0 = time.time()

"""
newtrains = []
for x in range(5):
    newtrains.append(stua.gtfsBus())
    newtrains[x].get("803147", 0, x+1)

for train in newtrains:
    print(f'{train.time} minutes ({train.route_id} to {train.terminus})')

print(time.time() - t0)
t0 = time.time()
"""


f = stua.gtfsBusBATCHED([("803147", 0, 1, 0), ("551529", 0, 2, 0), ("803147", 0, 3, 0)])
for train in f:
    print(f'{train.time} minutes ({train.route_id} to {train.terminus})')
print(time.time()-t0)