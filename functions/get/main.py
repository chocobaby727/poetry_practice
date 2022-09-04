from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main() -> Dict[str, str]:
    return {"msg": "Hello World"}
