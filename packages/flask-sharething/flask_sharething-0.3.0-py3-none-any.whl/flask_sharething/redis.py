from redis import Redis as _Redis
from .flask_redis import FlaskRedis as _FlaskRedis

redis = _FlaskRedis()
