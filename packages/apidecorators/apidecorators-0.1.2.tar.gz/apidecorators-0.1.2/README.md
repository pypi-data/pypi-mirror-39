# API Decorators

```python
# ctest.py
from apidecorators.api import jwt_auth, get, insert, has_role, update, push, pull, \
                validate, get_many, delete, read_access, write_access, collection, aggregate, \
                update_array, get_from_array              
from cerberus import Validator

public = {'*': '*'}

schema = {
    'a': {'type': 'string'},
    'b': {'type': 'integer'}
}

validator = Validator(schema)

schema_array = {
    'c': {'type': 'string'},
    #'__owner': {'type': 'string'}
}

validator_array = Validator(schema_array)

def set_routes_test(routes):

    @routes.post('/api/test')
    @jwt_auth
    @collection('test')
    @write_access(public)
    @validate(validator=validator)
    @insert
    async def post_test(document, request, payload):
        return document   

    @routes.get('/api/test/{_id}')
    @jwt_auth
    @collection('test')
    @read_access({'__owner': ['a']})
    @get
    async def get_test(document, payload):      
        return document

    @routes.put('/api/test/{_id}')
    @jwt_auth
    @collection('test')
    @write_access({'__owner': '*'})
    @validate(update=True, validator=validator)
    @update
    async def put_test(old_doc, document, request, payload):      
        return document

    @routes.put('/api/test/{_id}/array')
    @jwt_auth
    @collection('test')
    @write_access({'__owner': '*'})
    @validate(validator=validator_array)
    @push('array')
    async def push_array(document, request, payload):
        document['__owner'] = payload['user']      
        return document

    @routes.get('/api/test/{_id}/array')
    @jwt_auth
    @collection('test')
    @read_access({'__owner': ['c']})
    @get_from_array('array')
    async def get_test(document, payload):      
        return document

    @routes.put('/api/test/{_id}/array/{sub_id}')
    @jwt_auth
    @collection('test')
    @write_access({'__owner': ['c']}, root='array')
    @update_array('array')
    async def update_test(document, payload):      
        return document

    @routes.get('/api/test/aggregate/agg1')
    @jwt_auth
    @collection('test')
    @read_access({'__owner': ['__owner', 'length']})
    @get_many
    async def get_aggr_test(col, query, payload):  
        pipeline = [{"$match": {"b": 5}},
                    {"$project": {"__owner": 1, "length": {"$size": "$array"} }}
        ]
        return col.aggregate(pipeline)

#app.py
import asyncio
from ctest import set_routes_test
from aiohttp import web
from apidecorators.api import cors_factory


async def handle(loop):
    app = web.Application(loop=loop, middlewares=[cors_factory])
    routes = web.RouteTableDef()

    set_routes_test(routes)
    app.router.add_routes(routes)
    await loop.create_server(app.make_handler(), '0.0.0.0', 8888)

def main():    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle(loop))
    print("Server started at port 8888")
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
```

docker-compose.yml
```yml
version: '3'
services:
  api:
    build: .
    environment:
    - DB_URI=mongodb://<user>:<password>@url:port/data-base
    - DB=data-base
    - SECRET=secret
    stdin_open: true
    tty: true
    ports:
    - "8089:8089"
    volumes:
    - ./:/usr/src/app
    command: python -m watchgod app.main 
```
