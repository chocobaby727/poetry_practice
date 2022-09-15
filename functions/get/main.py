import json
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def save_openapi_json() -> None:
    openapi_json = app.openapi()
    print("start up called")

    with open("openapi.json", "w") as file:
        json.dump(openapi_json, file)


@app.get("/")
async def read_main() -> Dict[str, str]:
    return {"msg": "Hello World"}
