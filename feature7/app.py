import os
import uuid
import json
from flask import Flask, request, jsonify, render_template, stream_with_context, Response
from .pub import publish_message
import threading
from .progress_service import process_file
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


import redis
r = redis.Redis(host='localhost', port=6379, db=0)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    
    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    task_id = str(uuid.uuid4())
    threading.Thread(target=process_file, args=(task_id,), daemon=True).start()
    publish_message("channel1", json.dumps({"task_id": task_id, "message": f"File saved at {filepath}"}))
    message = f"File uploaded successfully: {file.filename}"
    return render_template("track_progress.html", message=message, task_id=task_id)


@app.route("/progress/<task_id>")
def progress_stream(task_id):
    def event_stream():
        pubsub = r.pubsub()
        pubsub.subscribe("channel1")
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode())
                yield f"data: {json.dumps(data)}\n\n"
                if data.get("status") == "done": 
                    break
    return Response(event_stream(), mimetype="text/event-stream")



if __name__ == "__main__":
    app.run(port=5000)