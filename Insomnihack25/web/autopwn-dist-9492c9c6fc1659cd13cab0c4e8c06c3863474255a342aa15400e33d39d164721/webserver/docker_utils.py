import docker
import secrets
import re

CONTAINER_IMAGE = "autopwn_scanner"
CONTAINER_PREFIX = "scanner_"

client_docker = docker.from_env()

def create_instance(command):
    instance_id = secrets.token_hex(8)
    container_name = CONTAINER_PREFIX + instance_id
    docker_created = client_docker.containers.run(CONTAINER_IMAGE, name=container_name, detach=True, command=command)
    if docker_created is not None:
        return instance_id
    else:
        return None

def get_logs_and_remove_if_exited(instance_ID):
    try:
        contianer = client_docker.containers.get(CONTAINER_PREFIX + instance_ID)
        logs = contianer.logs(stdout=True, stderr=False).decode('utf-8')
        print(logs)

        # remove extracted data after the URL
        matches = re.search(r"(.* https?://[^ ]*)", logs)
        if matches is not None:
            logs = matches.group(0)
        else:
            logs = ""

        if contianer.status == "exited":
            contianer.remove(force=True)
        return logs
    except docker.errors.NotFound:
        return None
