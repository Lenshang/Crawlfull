import io
import config
import threading
from fastapi import FastAPI, APIRouter, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.handler.file_handler import get_file, add_file
from core.handler.node_handler import reg_downloader_node
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from downloader.main import start_loop
from multiprocessing import Process, Value

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
    elif "json" in item.contentType:
        return JSONResponse(item.content, media_type=item.contentType)
    else:
        stream = io.BytesIO(item.content)
        return StreamingResponse(stream, media_type=item.contentType)


@api_router.post("/update")
async def update(file: UploadFile = File(...)):
    return add_file(file.file.read())


def create_service() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # on start 注册节点信息到REDIS
        reg_downloader_node(NODE_NAME, config.get("DOWNLOADER", "DOWNLOADER_SERVICE_URL"))
        # 启动下载进程
        running = Value("d", 1)
        loop_process = Process(target=start_loop, args=(running,))
        loop_process.start()
        yield
        # on close 关闭下载线程
        running.value = -1

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
