import json

from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def save_openapi_json() -> None:
    openapi_json = app.openapi()

    with open("openapi.json", "w") as file:
        json.dump(openapi_json, file)
