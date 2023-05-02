(In raw mode you could see the json objects corretcly)
****Group:

Praneeth Gubba pgubba@stevens.edu
Akash Adarsh a8@stevens.edu
Nithin Reddy Gutha ngutha@stevens.edu

***GitHub repo:

https://github.com/Praneethg23/FlaskProject

*****hours we spent on the project

We spent about 40 hours in total

****a description of how you tested your code

First we developed whole code including the extensions and used postman desktop version to test our code. We made two collections one tests basic endpoints,
while the other tests extensions. We added tests for the requests as well and everything worked fine. But Removed tests for requests which uses keys(randomly generated which will change each time we run the code as new server) but still placed the request and response we got.

*******any bugs or issues you could not resolve
We were unable to figure out a way  to do timely search.
As keys should be randomly generated and unique and also we didnt implement persistent extensions post keys and user keys change and for requests include this information they need to changed dynamically for each run.

********an example of a difficult issue or bug and how you resolved
We thought of creating endpoint which require json object as body which will have time fields so that we can search posts using this time.
a list of the four extensions you’ve chosen to implement

***Extensions
① Users and user keys
Here we implemented users to create posts using ther user_id and user_key. User need to give user_id,user_key along with message in request body as valid json
To create a post using user_id and user_key
POST http://127.0.0.1:5000/user

{
    "msg":"user 1 post 2",
    "user_id":0,
    "user_key":"vUY_n-Xy3F5BG8QWp8Herg"
}
return:
{
    "id": 1,
    "key": "P-47RbiXR9WqR3xD0liDYQ",
    "msg": "user 1 post 2",
    "timestamp": "2023-05-01T19:10:28.027316",
    "user_id": 0,
    "user_key": "vUY_n-Xy3F5BG8QWp8Herg",
    "username": "Praneeth"
}

deleting a post created by user
DELETE http://127.0.0.1:5000/post/2/delete/user/vUY_n-Xy3F5BG8QWp8Herg
return:
{
    "id": 2,
    "key": "KMkK729XO22vVULnHj-lSQ",
    "timestamp": "2023-05-01T19:16:53.385761",
    "user_id": 0,
    "username": "Praneeth"
}
Get a post created with user 
GET http://127.0.0.1:5000/post/2
return:
{
    "id": 2,
    "msg": "user 1 post 3",
    "timestamp": "2023-05-01T19:16:53.385761",
    "user_id": 0,
    "username": "Praneeth"
}
Creating a user
POST http://127.0.0.1:5000/user
{
    "username":"Praneeth",
    "name" :"Praneeth Gubba"
}
return:
{
    "name": "Praneeth Gubba",
    "user_id": 0,
    "user_key": "vUY_n-Xy3F5BG8QWp8Herg",
    "username": "Praneeth"
}
② User profiles.
Here for unique metadata we had a field called username and non-unique to be name. While creating a user we need to give username and user in request body as json object with string values.
They can be also edited using PUT request.
Creating a user
POST http://127.0.0.1:5000/user
{
    "username":"ladduRaman",
    "name":"Raman Sri"
}
return:
{
    "name": "Raman Sri",
    "user_id": 1,
    "user_key": "8LLmfG-RBK5NBZb0jMihkA",
    "username": "ladduRaman"
}
Editing a user
PUT http://127.0.0.1:5000/user/8LLmfG-RBK5NBZb0jMihkA
{
    "username":"raman"
}
return:
{
    "name": "Raman Sri",
    "user_id": 1,
    "username": "raman"
}
getting a user details using his username
GET http://127.0.0.1:5000/user/Praneeth
{
    "name": "Praneeth Gubba",
    "user_id": 0,
    "username": "Praneeth"
}
Get a post created with user 
GET http://127.0.0.1:5000/post/2
return:
{
    "id": 2,
    "msg": "user 1 post 3",
    "timestamp": "2023-05-01T19:16:53.385761",
    "user_id": 0,
    "username": "Praneeth"
}
③ Fulltext search

Visit http://127.0.0.1:5000/post/search/msg/<text>
GET http://127.0.0.1:5000/post/search/msg/post
return:
[
    {
        "id": 0,
        "msg": "user 1 post 1",
        "timestamp": "2023-05-01T19:09:07.420087",
        "user_id": 0,
        "username": "Praneeth"
    },
    {
        "id": 1,
        "msg": "user 1 post 2",
        "timestamp": "2023-05-01T19:10:28.027316",
        "user_id": 0,
        "username": "Praneeth"
    }
]
GET http://127.0.0.1:5000/post/search/msg/hello
return:
{
    "err": "not found"
}

④ User-based range queries 

Visit http://127.0.0.1:5000/post/search/user/<user_id>
examples:
http://127.0.0.1:5000/post/search/user/0
return:
[
    {
        "id": 0,
        "msg": "user 1 post 1",
        "timestamp": "2023-05-01T19:09:07.420087",
        "user_id": 0,
        "username": "Praneeth"
    },
    {
        "id": 1,
        "msg": "user 1 post 2",
        "timestamp": "2023-05-01T19:10:28.027316",
        "user_id": 0,
        "username": "Praneeth"
    }
]

http://127.0.0.1:5000/post/search/user/2
return:
{
    "err": "not found"
}
⑤ Date- and time-based range queries
Visit http://127.0.0.1:5000/post/search/time
This endpoint expects you to provide a json object in body which should have atleast-
-one of the fields startTime,endTime which should be valid date time string of format -
- of '%m/%d/%Y %H:%M:%S' or else it gives a bad request error.

examples:
GET http://127.0.0.1:5000/post/search/time
req.body:
{
    "endTime":"05/05/2023 23:13:57"
}
return:
[
    {
        "id": 0,
        "msg": "user 1 post 1",
        "timestamp": "2023-05-01T19:09:07.420087",
        "user_id": 0,
        "username": "Praneeth"
    },
    {
        "id": 1,
        "msg": "user 1 post 2",
        "timestamp": "2023-05-01T19:10:28.027316",
        "user_id": 0,
        "username": "Praneeth"
    }
]
req.body:
{
    "startTime":"04/28/2023 23:13:57"
}
return:
[
    {
        "id": 0,
        "msg": "user 1 post 1",
        "timestamp": "2023-05-01T19:09:07.420087",
        "user_id": 0,
        "username": "Praneeth"
    },
    {
        "id": 1,
        "msg": "user 1 post 2",
        "timestamp": "2023-05-01T19:10:28.027316",
        "user_id": 0,
        "username": "Praneeth"
    }
]
req.body:
{
    "startTime":"04/28/2023 23:13:57",
    "endTime":"05/05/2023 23:13:57"
}
return:
[
    {
        "id": 0,
        "msg": "user 1 post 1",
        "timestamp": "2023-05-01T19:09:07.420087",
        "user_id": 0,
        "username": "Praneeth"
    },
    {
        "id": 1,
        "msg": "user 1 post 2",
        "timestamp": "2023-05-01T19:10:28.027316",
        "user_id": 0,
        "username": "Praneeth"
    }
]
req.body:
{
}
return:
{
    "err": "bad request"
}
req.body:
{
    "endTime":"04/28/2023 23:13:57"
}
return:
{
    "err": "not found"
}

******detailed summaries of your tests for each of your extensions

test 1
For the tests we basically gave different kind of requests and for requests whgich didnt needed keys have been tested with the predefined test cases and for 
requests with keys they were manually examined (response).
We placed our requests and responses we got in the collections and also predefined tests on them.
newman run basic_endpoints_testing.postman_collection.json

In this we created posts and also tested with bad requests
Retrived the posts using GET and also tested for error cases
Reuqets for delete both correct and wrong requests have been tested here.

test 2

newman run extensions_testing.postman_collection.json

In this we created users, edited users and tried ti retrive user using endpoints and also tested false cases.
We created posts using user fields.
Requests to search for posts created by a user using user id both correct and incorrect inputs were tested
Requests to search posts using text 
Requests to search posts by the timestamp of posts with given start and end time.

