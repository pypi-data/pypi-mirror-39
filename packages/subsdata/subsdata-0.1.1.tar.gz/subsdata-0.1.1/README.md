# SDP: Subscription Data Protocol

```python
import asyncio
import websockets
from rethinkdb import r
from subsdata.sdp import sdp, method, sub, get_connection

@method
async def add(user, a, b):
    return a + b

@method
async def create(user):
    connection = await get_connection()
    await r.table('test').insert({'x': 0}).run(connection)

@method
async def increment(user, id, value):
    connection = await get_connection()
    await r.table('test').get(id).update({"x": r.row["x"]+value}).run(connection)

@sub
def x_less_than(user, max):
    return r.table('test').filter(lambda row: (row['x'] < max))

def main():    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(sdp, '0.0.0.0', 8888))
    print("Real time server started at port 8888")
    loop.run_forever()
    loop.close()
```

```yml
#example of a docker-compose.yml
version: '3'
services:
  ws:
    build: .
    stdin_open: true
    tty: true
    ports:
    - "8888:8888"
    volumes:
    - ./:/usr/src/app
    environment:
    - RT=rdb
    - DEBUG=1
    - SECRET=secret
    command: python -m watchgod app.main 
  rdb:
    image: rethinkdb
    ports:
    - "8080:8080"
    - "28015:28015"
    volumes:
    - './data:/data'
```