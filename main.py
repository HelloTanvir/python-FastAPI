# run uvicorn main:app --reload to start the server

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, responses

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
        """
    )


@app.get("/about")
def about():
    return {"message": "This is a FastAPI tutorial"}


@app.get("/html")
def html():
    return responses.FileResponse("./template/index.html")
