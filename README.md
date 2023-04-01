# Talkanon 🕵️‍♂️💬
Talk to People Anonymously!

Do you want to let your thoughts out into the world without showing your identity? 
These days, every activity you do online will leave a digital footprint where it can be stored for a long time.
With **Talkanon**, you can chat with people worldwide anonymously.

This service runs asynchronously by using RabbitMQ queue, where new messages are stored before consumed by a separate worker thread which saves it to the database.
The approach makes sure that every message will be recorded in exact chronological order.


## 📌 Instructions
Currently, the service is hosted on [34.30.125.161](http://34.30.125.161). Postman collection can be accessed [here](https://elements.getpostman.com/redirect?entityId=12147807-b65f2a41-d66c-48c7-b6cf-9d4d3ef1e725&entityType=collection).

There are 4 main flows/features in this service:

### 1. Get list of rooms
#### HTTP GET /rooms
Returns list of available chat rooms.

#### Response Format:
```
[{
  "id": int - chat room's id,
  "timestamp": date - latest update,
  "messages" []
}]
```

#### Sample Request:

> [http://34.30.125.161/rooms](http://34.30.125.161/rooms)

#### Sample Response:
```
[{
  "id": 1,
  "timestamp": "2023-04-01T06:44:12.469921",
  "messages": [],
}]
```

### 2. Create new room
#### HTTP POST /rooms
Returns the newly created room.

#### Response Format:
```
{
  "id": int - chat room's id,
  "timestamp": date - latest update,
  "messages" []
}
```

#### Sample Request:

```curl
curl -X POST 'http://34.30.125.161/rooms'
```

#### Sample Response:
```
{
  "id": 2,
  "timestamp": "2023-04-01T06:44:12.469921",
  "messages": [],
}
```

### 3. Get list of messages
#### HTTP GET /rooms/{room_id}/messages
Returns list of messages in room `room_id`.

#### Response Format:
```
[{
  "id": int - message's id,
  "content": str - message's content,
  "timestamp": date - message's sent timestamp,
  "room_id": int - current room's id
}]
```

#### Sample Request:

> [http://34.30.125.161/rooms/1/messages](http://34.30.125.161/rooms/1/messages)

#### Sample Response:
```
[{
  "id": 1,
  "content": "Hello World",
  "timestamp": "2023-04-01T08:24:54.400439",
  "room_id": 1
}]
```

### 4. Send message
#### HTTP POST /rooms/{room_id}/messages?content={content}
Send a new anonymous message to a room `room_id`.

#### Response Format:
```
"ok"
```

#### Sample Request:

```curl
curl -d 'content=Hello' -X POST 'http://34.30.125.161/rooms/1/messages'
```

#### Sample Response:
```
"ok"
```


## 💻 Development
To run on your local environment, first ask me [here](mailto:marcellinocovara@gmail.com) for the `.env` file and make sure to have [docker](https://docker.com) installed.

Go to the root directory and run:
```
docker compose up -f docker-compose.dev.yml -d --build
```


## 🚀 Deployment
To run on production environment, run:
```
docker compose up -d --build
```
