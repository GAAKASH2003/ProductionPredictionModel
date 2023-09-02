from sklearn.model_selection import train_test_split
from fastapi import FastAPI, UploadFile, File
import numpy as np
import joblib
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import bz2file as bz2
from fastapi import HTTPException
app = FastAPI()

origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods = ['*'],
    allow_headers  = ['*']
)
def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as f:
        data = pickle.load(f)
    return data

# model = joblib.load(model)


col=pd.read_csv("crop_production.csv")

doop = pd.read_excel("cols.xlsx")
states={}
j=0
for i in col["State_Name"].unique():
    states[j]="State_Name_"+i
    j=j+1
    
j=0    
seasons={}
for i in col["Season"].unique():
    seasons[j]="Season_"+i
    j=j+1
j=0
crops={}
for i in col["Crop"].unique():
    crops[j]="Crop_"+i
    j=j+1

def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as data:
        data = pickle.load(data)
    return data

file=decompress_pickle("yield2.pbz2")




# pickle.dump(model,open('https://drive.google.com/file/d/12-zDK3Wqzjy1KhPVrAruSjh-xPFWqF4C/view?usp=sharing','wb'))
# produce=pickle.load(open('https://drive.google.com/file/d/12-zDK3Wqzjy1KhPVrAruSjh-xPFWqF4C/view?usp=sharing','rb'))    
    
# produce.predict(doop)    
@app.get("/")
def index():
    return {"Message":"Hello world"}

@app.post("/predict")
def predict(data: dict):
    crop_name = data.get('crop_name')
    state = data.get('state')
    season = data.get('season')
    area=data.get('area')
    doop[states[state]]=1
    doop[crops[crop_name]]=1
    doop[seasons[season]]=1 
    doop['Area']=area 
    prediction = file.predict(doop)
    print(doop.shape)
    return {"prediction": prediction.tolist()}
        

'''
{
    "crop_name":1,
    "season":3,
    "state":4,
    "area":48
}
'''