# Import dependencies
import requests;
import pymongo;

# APPID = 65f2c79f926c225353acd8a9
# Step 1 Function to fetch User Data from API end point
# API endPoint = https://dummyapi.io/data/v1/user
def fetchUserData(appId):
    URL = 'https://dummyapi.io/data/v1/user'
    headers = {'app-id': appId}
    response = requests.get(url= URL, headers=headers)
    data = response.json()
    return data

# Step 2 Function to fetch User's post data from apiendpoint
# API endpoint = https://dummyapi.io/data/v1/user/{{user_id}}/post
def fetchUsersPostData(appId, userId):
    URL = f'https://dummyapi.io/data/v1/user/{userId}/post'
    headers = {'app-id': appId}
    response = requests.get(url= URL, headers= headers)
    data = response.json()
    return data

# Step 3 Make mongoDB connection
mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
db = mongoClient["TailNode"]

# Step 4 Fetch the users data and store it in a variable
appID = '65f2c79f926c225353acd8a9'
userData = fetchUserData(appID)

# Step 5 Store user data into mongoDB
userCollection = db["users"]
userCollection.insert_many(userData['data'])

# Step 6 Fetch users post data and store it into mongoDB
for user in userData['data']:
    userPost = fetchUsersPostData(appID, user['id'])
    postCollection = db[f'user_{user['id']}_posts']
    postCollection.insert_many(userPost['data'])