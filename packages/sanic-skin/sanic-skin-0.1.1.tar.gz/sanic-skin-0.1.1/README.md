# sanic_skin
A wrapper for sanic in order to code in a tornado-like way<br>

Sanic is a flask-like python web framework, I write this module to enable a easy way which make Sanic act like a tornado one.<br>
I also make postgresql and redis easy-use interface in it.<br>

## installation
* pip install sanic-skin<br>
## usage
Use SanicSkin instead of Sanic to instantiate. I add three optional parameters:<br>
* url_patterns is a list object including tuple url-handler pairs,<br>
* settings is a dict object of your own settings,<br>
* enable_dbs is a list object which you can add 'pg' or 'redis'.<br>

When you want to access db in handlers, you can use request.app._skin.pg/redis to achieve safe using of db which is a simplified way of using asyncpg and aioredis in which you have to always use async with statement.<br>

## Example:<br>
```python
from sanic_skin import SanicSkin
from sanic.response import text


settings = {'PG':{
    'host':'127.0.0.1',
    'port':5432,
    'user':'postgres',
    'password':'postgres',
    'database':'dataview',
    'min_size':10,
    'max_size':10,
  },
  'REDIS':{
    'address':('127.0.0.1', 6379),
    'db':0,
    'minsize':10,
    'maxsize':10,
  }
}

async def test(request):
    result = await request.app._skin.redis('get', 'key')
    return text(result)

app = SanicSkin(__name__, url_patterns=[
    (r'/', test),
    (r'/test', test),
], settings=settings, enable_dbs=['pg', 'redis'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```
