from redis import Redis as _Redis, ConnectionPool as _ConnectionPool


class FlaskRedis(_Redis):
    def __init__(self, app=None, **kwargs):
        self.connection_pool = None
        self.response_callbacks = self.__class__.RESPONSE_CALLBACKS.copy()
        self._kwargs = kwargs

        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')

        self._kwargs.update(kwargs)
        self.connection_pool = _ConnectionPool.from_url(redis_url, **self._kwargs)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['redis'] = self
