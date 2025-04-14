#!/usr/bin/env python3
from flask import Flask, send_from_directory, render_template, request
from celery import Celery
import redis
from flask_limiter import Limiter
from secrets import token_hex
import os
import re
import docker_utils
import docker
import glob
client_docker = docker.from_env()
CONTAINER_PREFIX = "scanner_"
CONTAINER_IMAGE = "autopwn_scanner"

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379").strip()
SCAN_PREFIX = "scan_"

TEMPLATE_LIST = [t.replace("/app/nuclei-templates/", "").replace(".yaml", "") for t in glob.glob("/app/nuclei-templates/**/*.yaml", recursive=True)]

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or token_hex(16)

celery = Celery(app.import_name, broker=REDIS_URL, backend=REDIS_URL)

r = redis.Redis.from_url(REDIS_URL)


def get_remote_address():
    return request.remote_addr

limiter = Limiter(get_remote_address,
                  app=app,
                  default_limits=["60 per minute", "10 per second"],
                  storage_uri="memory://")

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        client_ip=get_remote_address(),
        template_list=TEMPLATE_LIST
    )

@app.route("/static/<path:path>", methods=["GET"])
def static_file(path):
    return send_from_directory("static", path)

@app.route('/scan', methods=['POST'])
@limiter.limit("2 per minute; 10 per 10 minutes")
def scan():
    target = get_remote_address()
    template = request.form.get("template")
    if template not in TEMPLATE_LIST:
        return "Invalid template", 400

    command = f"-u http://{target}:1337 -t {template}.yaml -timestamp -no-color -matcher-status -headless -disable-redirects -timeout 30 -silent"
    instance_id = docker_utils.create_instance(command=command)

    r.set(SCAN_PREFIX + instance_id, 'Scanning...')

    return {"task_id": instance_id}

@app.route('/scan/<scan_id>')
@limiter.limit("1 per second")
def get_scan_status(scan_id):
    if not validate_scan_id(scan_id):
        return "Invalid scan ID", 400

    logs = docker_utils.get_logs_and_remove_if_exited(scan_id)
    if logs is not None:
        r.set(SCAN_PREFIX + scan_id, logs)
        return {"logs": logs, "status": "in_progress"}
    
    logs = r.get(SCAN_PREFIX + scan_id)
    if logs is not None:
        return {"logs": logs.decode('utf-8'), "status": "completed"}
    else:
        return {"status": "not_found"}

def validate_scan_id(scan_id):
    return re.match(r"^[a-f0-9]{16}$", scan_id) is not None

if __name__ == "__main__":
    app.run(debug=True)
