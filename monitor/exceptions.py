from starlette.requests import Request
from starlette.responses import JSONResponse


async def generic_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 103,
            "message": f"服务器错误：{exc}"
        }
    )
