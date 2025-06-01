from fastapi import FastAPI
from threading import Thread
import os
from watcher import watch_folder

app = FastAPI()
FOLDER_TO_WATCH = "./templates"

@app.on_event("startup")
async def startup_event():
    watcher_thread = Thread(target=watch_folder,args=(FOLDER_TO_WATCH), daemon=True)
    watcher_thread.start()

@app.get("/")
async def read_root():
    return {"message": "Folder watcher is running"}

