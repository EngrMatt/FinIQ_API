# app/__init__.py
from fastapi import FastAPI
from .routers import (
    user_router, 
    auth_router
    )

def create_app() -> FastAPI:
    app = FastAPI(title="FinIQ API")

    # 將所有 router 放到列表中
    routers = [
        user_router.router,
        auth_router.router,
        # product_router.router,
        # order_router.router,
        # 未來新增 router 直接加到這裡
    ]

    for r in routers:
        app.include_router(r)

    return app
