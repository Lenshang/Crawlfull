import uvicorn
import config
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.handler.file_handler import reg_downloader_node, get_file
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

api_router = APIRouter()
NODE_NAME = config.get("DOWNLOADER", "NODE_NAME")


@api_router.get("/test")
async def test():
    return "OK"


@api_router.get("/get")
async def get(id: str):
    item = get_file(id, NODE_NAME)
    if "text" in item.contentType:
        return HTMLResponse(item.content, media_type=item.contentType)
    elif "json" in item.conteType:
        return JSONResponse(item.content, media_type=item.contentType)
    else:
        return FileResponse(item.content, media_type=item.contentType)


def create_service() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # on start
        # 注册节点信息到REDIS
        reg_downloader_node(NODE_NAME, config.get("DOWNLOADER", "DOWNLOADER_SERVICE_URL"))
        # TODO 启动下载进程
        yield
        # on close
        # TODO 关闭下载进程

    application = FastAPI(title="Crawlfull-Downloader RestApi", lifespan=lifespan)
    application.debug = True

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex="https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api")

    return application
