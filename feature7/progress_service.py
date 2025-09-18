import json
import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def process_file(task_id):
    total_steps = 100
    for _ in range(total_steps):
        time.sleep(0.1)  # simulate work
        progress = {
            "service": "process_file",
            "task_id": task_id,
            "status": "processing",
            "message": "Processing..."
        }
        r.publish("channel1", json.dumps(progress))

    # done message
    r.publish("channel1", json.dumps({
        "task_id": task_id,
        "status": "done",
        "message": "Task completed"
    }))
