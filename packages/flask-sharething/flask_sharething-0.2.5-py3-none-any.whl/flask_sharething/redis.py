from flask_redis import FlaskRedis as _FlaskRedis
from redis import Redis

redis: Redis = _FlaskRedis()

