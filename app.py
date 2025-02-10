from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from config import MONITOR_SQL_HOST, MONITOR_SQL_PORT, MONITOR_SQL_AUTHENTICATION, MONITOR_SQL_DATABASE
from monitor.exceptions import generic_exception_handler
from monitor.middlewares import RequestIDMiddleware
from monitor.router import router as resource_router


def create_app():
    app = FastAPI(title="ResourceMonitor")

    app.include_router(resource_router, prefix="/tax/monitor/resource")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(RequestIDMiddleware)

    app.add_exception_handler(Exception, generic_exception_handler)
    return app


monitor_app = create_app()
register_tortoise(
    monitor_app,
    db_url=f"mysql://{MONITOR_SQL_AUTHENTICATION}@{MONITOR_SQL_HOST}:{MONITOR_SQL_PORT}/{MONITOR_SQL_DATABASE}",
    modules={
        "models": [
            "monitor.models"
        ]
    },
    generate_schemas=False,
    add_exception_handlers=True
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(monitor_app, host="0.0.0.0", port=8000)
