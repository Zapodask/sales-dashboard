from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import (
    category_router,
    dashboard_router,
    health_router,
    order_router,
    product_router,
)


class Api:
    def __init__(self):
        self.app = FastAPI()

        self.__apply_middlewares()
        self.__append_routes()

    def __append_routes(self):
        self.app.include_router(category_router)
        self.app.include_router(dashboard_router)
        self.app.include_router(health_router)
        self.app.include_router(order_router)
        self.app.include_router(product_router)

    def __apply_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        pass
