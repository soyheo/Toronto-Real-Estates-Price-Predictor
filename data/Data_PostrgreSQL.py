import psycopg2
from pymongo import MongoClient
import sqlite3
import json
from dotenv import load_dotenv
import os

# MongoDB data retrieving
load_dotenv()
host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
db_name = os.getenv('DATABASE_NAME')
col_name = os.getenv('COLLECTION_NAME')
mongo_uri = f"mongodb+srv://{user}:{password}@{host}/{db_name}?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client[db_name]
coll = db[col_name]
docs = coll.find({}, {'_id':False})

listing_list = []
id_list = []
building_list = []
property_list = []
for i in range(1, len(docs)):
    for j in range(len(docs[i]['Results'])):
        id = docs[i]['Results'][j]['Id']
        building = docs[i]['Results'][j]['Building']
        property = docs[i]['Results'][j]['Property']
        listing_list.append({"id": id, "building": building, "property": property})
        try: 
            building_list.append((
                id, 
                building.get('BathroomTotal'), 
                building.get('Bedrooms'),
                building.get('Type'),
                building.get('Ammenities')
                ))
            
            property_list.append((
                id, 
                property.get('Price').replace(',', '').replace('$', ''), 
                property.get('Type'),
                property.get('Address').get('AddressText'),
                property.get('Address').get('Longitude'),
                property.get('Address').get('Latitude'),
                property.get('ParkingSpaceTotal'),
                property.get('ParkingType'),
                property.get('OwnershipType'),
                property.get('AmmenitiesNearBy')
                ))
            
        except KeyError:
            print("key_error")

# print(property_list)



# Connect to postgresql db
host=os.getenv("PG_host")
dbname=os.getenv("PG_dbname")
user=os.getenv("PG_user")
password=os.getenv("PG_password")
port=os.getenv("PG_port")

conn = psycopg2.connect(f"host={host} dbname={dbname} user={user} password={password} port={port}")
cur = conn.cursor()


# Create postgresql table
create_table1 = """CREATE TABLE Building(
                        Id INTEGER NOT NULL PRIMARY KEY,
                        BathroomTotal INTEGER,
                        Bedrooms VARCHAR(20),
                        Type VARCHAR(30),
                        Ammenities VARCHAR(100)
                        );"""

create_table2 = """CREATE TABLE Property (
                        Id INTEGER NOT NULL PRIMARY KEY,
                        Price INTEGER,
                        Type VARCHAR(20),
                        AddressText VARCHAR(100),
                        Longitude FLOAT,
                        Latitude FLOAT,
                        ParkingSpaceTotal INTEGER,
                        ParkingType VARCHAR(100),
                        OwnershipType VARCHAR(30),
                        AmmenitiesNearBy VARCHAR(100),
                        CONSTRAINT Id_fk FOREIGN KEY(Id)
                        REFERENCES Building(Id)
                        ON DELETE CASCADE
                        )"""


drop_table_if_exists_1 = "DROP TABLE IF EXISTS Building;"
drop_table_if_exists_2 = "DROP TABLE IF EXISTS Property;"

cur.execute(drop_table_if_exists_2)
cur.execute(drop_table_if_exists_1)


cur.execute(create_table1)
cur.execute(create_table2)

conn.commit()



# Insert data into postgresql
cur.executemany("INSERT INTO Building VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", building_list)
cur.executemany("INSERT INTO Property VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", property_list)
conn.commit()

# cur.execute("SELECT * FROM building")
# data = cur.fetchall()

conn.close()

# print(data)