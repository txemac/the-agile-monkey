from http import HTTPStatus
from typing import Dict

import uvicorn
from fastapi import FastAPI

from database import Base
from database import engine

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    api = FastAPI(
        title="The CRM service API",
    )

    return api


app = create_app()


@app.get("/health", status_code=HTTPStatus.OK)
def get_check() -> Dict:
    return dict(status="OK")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
