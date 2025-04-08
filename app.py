import os

from flask import Flask
import redis

app = Flask(__name__)

redis_connection = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis-server:6379/0"))


@app.route("/ping")
def ping():
    return {"status": "ok"}


@app.route("/count")
def count_views():
    key = "page_views"

    if redis_connection.exists(key):
        count = redis_connection.incr(key)
    else:
        count = 1
        redis_connection.setex(key, 60, count)
    return f"Количество посещений страницы за 60 секунд: {count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)