import os
import uuid

UPLOAD_DIR = "/upload"
HTML_DIR = "./static"

filename = "../../../test"
uuid_val = str(uuid.uuid4())
folder = os.path.join(UPLOAD_DIR, uuid_val)

file_path = os.path.join(folder, filename) 
print(file_path)
#return {"uuid": f"{uuid_val}"}