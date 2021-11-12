from http import HTTPStatus
from typing import Dict

from fastapi import FastAPI

from customer.infrastructure.views.customer_views import api_customers
from main_schema import SchemaHealth
from user.infrastructure.views.auth_views import api_auth
from user.infrastructure.views.user_views import api_users


def create_app() -> FastAPI:
    api = FastAPI(
        title="The CRM service API",
    )

    api.include_router(api_auth, prefix="/auth", tags=["Auth"])
    api.include_router(api_users, prefix="/users", tags=["Users"])
    api.include_router(api_customers, prefix="/customers", tags=["Customers"])

    return api


app = create_app()


@app.get(
    path="/health",
    status_code=HTTPStatus.OK,
    response_model=SchemaHealth,
    tags=["Health"],
)
def get_check() -> Dict:
    return dict(status="OK")


if __name__ == "__main__":
    import uvicorn

    app.debug = True
    uvicorn.run(app, host="0.0.0.0", port=8000)
