import redis
import time
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def publish_message(channel, file):
    r.publish(channel, file)
    print(f"Published '{file}' to {channel}")
