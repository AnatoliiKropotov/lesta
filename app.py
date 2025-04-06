import os

from flask import Flask
from flask_caching import Cache
import redis

config = {
    "DEBUG": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_REDIS_URL": "redis://redis-server:6379/0"
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/ping")
def ping():
    return {"status": "ok"}


@app.route("/count")
def count():
    redis_connection = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis-server:6379/0"))
    count_connection = redis_connection.get("count")
    if count_connection is None:
        count_connection = 0
    count_connection += 1
    redis_connection.set("count", count_connection)
    return f"Количество посещений: {count_connection }"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
