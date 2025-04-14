from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse

from anyio.lowlevel import RunVar
from anyio import CapacityLimiter

import os
import uuid
import random
import signal

import io

UPLOAD_DIR = "/upload"
HTML_DIR = "./static"

app = FastAPI()

@app.on_event("startup")
def startup():
    print("start")
    RunVar("_default_thread_limiter").set(CapacityLimiter(1))

@app.middleware("http")
async def renew_worker(request: Request, call_next):
    response = await call_next(request)
    os.kill(os.getpid(), signal.SIGTERM)
    return response


@app.get("/")
def read_root():
    return FileResponse(f"{HTML_DIR}/index.html")

@app.post("/upload")
def upload(file: UploadFile):
    try:
        contents = file.file.read()
        print(contents, flush=True)
        uuid_val = str(uuid.uuid4())
        folder = os.path.join(UPLOAD_DIR, uuid_val)
        print(folder, flush=True)
        os.mkdir(folder)
        file_path = os.path.join(folder, file.filename)
        print(file_path, flush=True)
        with open(file_path, "wb") as f:
            f.write(contents)
        return {"uuid": f"{uuid_val}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.get("/download/{uuid_val}")
def view(uuid_val):
    try:
        u = str(uuid.UUID(uuid_val, version=4))
        d = os.path.join(UPLOAD_DIR, u)
    except:
        raise HTTPException(status_code=500, detail="Supplied value is not a valid UUID")
    if not os.path.isdir(os.path.join(UPLOAD_DIR, u)):
        raise HTTPException(status_code=404, detail="UUID not found")
    try:
        filename = os.listdir(d)[0]
        return FileResponse(os.path.join(d, filename))
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


