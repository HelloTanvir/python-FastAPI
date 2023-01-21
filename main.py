# run uvicorn main:app --reload to start the server

import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, responses

load_dotenv()

app = FastAPI()

user_name = os.environ["NAME"]


@app.get("/")
def say_hello(name: str = user_name):
    hint_msg = "<p>You can pass your name in the query parameter. For example: /?name=Tanvir</p>"
    info_msg = "<p>Click the button below to see the HTML page</p>"

    if name is name == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    return responses.HTMLResponse(
        f"""
            <h3>Hello {name}</h3>
            {name == user_name and hint_msg or info_msg}
            <button onclick="location.href='/html'" {name == user_name and "disabled" or ''}>Click me</button>
            <a href="/upload">Upload file</a>
        """
    )


@app.get("/about")
def about():
    return {"message": "This is a FastAPI tutorial"}


@app.get("/html")
def html():
    return responses.FileResponse("./template/index.html")


@app.get("/upload")
def upload():
    return responses.FileResponse("./template/upload.html")


@app.post("/upload-file")
def upload_file(file: UploadFile):
    directory_path = './uploads'

    print(file.filename)
    if file.filename is not None:
        print(file.filename)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    with open(f'{directory_path}/{file.filename}', "wb") as f:
        f.write(file.file.read())

    return responses.RedirectResponse(url=f"/see-file/?file={directory_path}/{file.filename}", status_code=302)


@app.get("/see-file")
def see_file(file: str):
    return responses.FileResponse(file)