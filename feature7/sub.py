import redis
import ast
import json 
import queue
r = redis.Redis(host='localhost', port=6379, db=0)
queue_event = queue.Queue()


def subscribe_channel(channel, service_name, operation):
    pubsub = r.pubsub() #creates a Redis Pub/Sub object.
    pubsub.subscribe(channel)
    print(f"[{service_name}] Subscribed to {channel}")
    
    # pubsub.listen() it generator yield publish_message message.
    for message in pubsub.listen():
        if message['type'] == 'message':
            msg_dict = json.loads(message['data'].decode())
            queue_event.put(msg_dict)
            task_id = msg_dict.get("task_id")
            text = msg_dict.get("message")
            
            if text:
                result = operation(text)
                print(f"[{service_name}] Task {task_id} → Received: {text} → Result: {result}")
        
            