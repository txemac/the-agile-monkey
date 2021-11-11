from http import HTTPStatus
from typing import Dict

from fastapi import FastAPI

from database import Base
from database import engine
from main_schema import Health

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    api = FastAPI(
        title="The CRM service API",
    )

    return api


app = create_app()


@app.get(
    path="/health",
    status_code=HTTPStatus.OK,
    response_model=Health,
    tags=['Health'],
)
def get_check() -> Dict:
    return dict(status="OK")


if __name__ == "__main__":
    import uvicorn

    app.debug = True
    uvicorn.run(app, host="0.0.0.0", port=8000)
