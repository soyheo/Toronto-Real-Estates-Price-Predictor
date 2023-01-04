import psycopg2
from pymongo import MongoClient
import sqlite3
import json

# MongoDB 데이터 불러오기
HOST = 'cluster1.leos9pf.mongodb.net'
USER = 'soyheo'
PASSWORD = 'soyheo1234'
DATABASE_NAME = 'Project'
COLLECTION_NAME = 'realtor_api'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
coll = db[COLLECTION_NAME]
docs = coll.find({}, {'_id':False})

listing_list = []
id_list = []
building_list = []
property_list = []
for i in range(1, 51):
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



# postgresql db 연결
conn = psycopg2.connect("host=localhost dbname=project user=postgres password=5846 port=5432")
cur = conn.cursor()


# postgresql 테이블 생성
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



# postgresql 데이터 삽입
cur.executemany("INSERT INTO Building VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", building_list)
cur.executemany("INSERT INTO Property VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", property_list)
conn.commit()

# cur.execute("SELECT * FROM building")
# data = cur.fetchall()

conn.close()

# print(data)