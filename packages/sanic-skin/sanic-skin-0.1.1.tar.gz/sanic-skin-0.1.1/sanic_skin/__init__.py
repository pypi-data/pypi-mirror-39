from sanic import Sanic
from sanic import Blueprint
import asyncpg, aioredis


class AppSkin(type):
    def __call__(cls, *args, **kargs):
        try:
            skargs = dict(kargs);skargs.pop('url_patterns', None)
            skargs.pop('settings', None);skargs.pop('enable_dbs', None)
            app = Sanic(*args, **skargs)
        except TypeError: # handle parameters error, in order to accept arbitrary parameters
            app = Sanic()
        app._skin = cls.__new__(cls, app) # ref to a instance of SanicSkin, so app can get func from SanicSkin
        app.config.update(kargs.get('settings') or {})
        app._skin.registerUrlPattern(kargs.get('url_patterns', []))
        app._skin.registerDb(kargs.get('enable_dbs', []))
        return app

class SanicSkin(metaclass=AppSkin):
    def __new__(cls, app):
        me = super().__new__(cls)
        me.app = app
        return me

    async def pg(self, method, *arg, **karg):
        async with self.app._pgpool.acquire() as conn:
            result = await type(conn).__dict__[method](conn, *arg, **karg)
        return result
    
    async def redis(self, *arg, **karg):
        async with self.app._redispool.get() as conn:
            result = await conn.execute(*arg, **karg)
        return result

    def registerUrlPattern(self, pattern):
        router = Blueprint(__name__)
        for path, handler in pattern:
            if isinstance(handler, str):
                router.static(path, handler)
            else:
                router.add_route(handler, path)
        self.app.blueprint(router)

    def registerDb(self, dbs):
        async def register_pg(app, loop):
            self.app._pgpool = await asyncpg.create_pool(**self.app.config.PG)
        async def register_redis(app, loop):
            self.app._redispool = await aioredis.create_pool(**self.app.config.REDIS)
        db_reg_map = {'pg':register_pg, 'redis':register_redis}
        async def close_pg(app, loop):
            await self.app._pgpool.close()
        async def close_redis(app, loop):
            self.app._redispool.close()
            await self.app._redispool.wait_closed()
        db_close_map = {'pg':close_pg, 'redis':close_redis}
        for db in dbs:
            self.app.register_listener(db_reg_map[db], 'before_server_start')
            self.app.register_listener(db_close_map[db], 'after_server_stop')

