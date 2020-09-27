from firebase import firebase
import json

firebase = firebase.FirebaseApplication("https://admob-api-bf0c8.firebaseio.com/", None)

with open('datas.json') as json_file:
    datas = json.load(json_file)

#Give Column name where new instance is going to be created
result = firebase.post('/AdMoB', datas)

print(result)