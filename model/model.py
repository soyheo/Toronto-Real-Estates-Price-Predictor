import psycopg2
import pandas as pd
# from sqlalchemy import create_engine
# import seaborn as sns
from sklearn.model_selection import train_test_split
import numpy as np
from xgboost import XGBRegressor
from sklearn.preprocessing import PowerTransformer
from category_encoders import OrdinalEncoder, OneHotEncoder
from sklearn.compose import TransformedTargetRegressor
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
import joblib
import pickle

conn = psycopg2.connect("host=localhost dbname=project user=postgres password=5846 port=5432")
cur = conn.cursor()
cur.execute("""SELECT * FROM building b 
JOIN property p USING (id)""")
json_data = cur.fetchall()
df = pd.DataFrame(json_data)
df.columns = ['id', 'bathroomtotal', 'bedrooms', 'type_x', 'ammenities', 'price', 'type_y', 'addresstext', 'longitude', 'latitude', 'parkingspacetotal', 'parkingtype', 'ownershiptype', 'ammenitiesnearby']
# print(df)

'''
# engine = create_engine('postgresql://postgres:5846@localhost:812/project')
# conn = engine.connect()
data_building = pd.read_sql("SELECT * FROM building", con=conn)
data_property = pd.read_sql("SELECT * FROM property", con=conn)
df = pd.merge(data_building, data_property, on='id')
print(df)
df.to_csv('real_estate_listing', index = False)
conn.close()
'''
# df = pd.read_csv(".\\database\\real_estate_listing")
# print(df)
# type_y의 Vacant Land와 Parkining 삭제
df = df.drop(df[(df.type_y == 'Vacant Land') | (df.type_y == 'Parking')].index)
# type_y 칼럼 전체 삭제
df = df.drop(['type_y'], axis=1)
# bedrooms 결측값 확인 및 삭제
df[df.bedrooms.isnull()]
df = df.drop(df[df.bedrooms.isnull()].index)
# 컬럼 데이터 타입 및 이름 변경
df.bathroomtotal = df.bathroomtotal.astype('int')
df.price = df.price.astype('float')
df.rename(columns={'type_x':'type'}, inplace=True)

# 데이터 분리 for modeling

train, test = train_test_split(df, train_size=0.80, test_size=0.20, random_state=2)
train.shape, test.shape
# train, val = train_test_split(train, train_size=0.80, test_size=0.20, random_state=2)


target = 'price'
features = ['bathroomtotal', 'parkingspacetotal', 'longitude', 'latitude', 'type']
X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

# API 구동을 위한 최종모델 선정
# 데이터 분리 for modeling
train, test = train_test_split(df, train_size=0.80, test_size=0.20, random_state=2)
train.shape, test.shape

target = 'price'
features = ['bathroomtotal', 'parkingspacetotal', 'longitude', 'latitude']
X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]
# Gradient Boosting 모델 분석

boosting = XGBRegressor(
    n_estimators=2000,
    objective='reg:squarederror', # default
    learning_rate=0.2,
    n_jobs=-1,
    max_depth=5,
    # early_stopping_rounds=100
)

pipe = make_pipeline(
    OneHotEncoder(), 
    SimpleImputer(),  
    boosting
)
model = TransformedTargetRegressor(regressor=pipe,
                                func=np.log1p, inverse_func=np.expm1)
model.fit(X_train, y_train)
# model.predict([[7, 2, -79, 43]])
# model = joblib.load('./model.pkl')
# data = {'bathroomtotal': [7],'parkingspacetotal': [2],'longitude': [-79.3415799374804], 'latitude': [43.769366531539454]}
# df_test = pd.DataFrame(data)
# print(model.predict(df_test))


# 모델 부호화


with open('model.pkl','wb') as pickle_file:
    pickle.dump(model, pickle_file)



