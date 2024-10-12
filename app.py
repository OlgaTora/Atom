from contextlib import asynccontextmanager

import aiofiles
from docx import Document
from fastapi import FastAPI, File, UploadFile, Request
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from splitter import Splitter
from vector_store import VectorStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    yield
    print("shutdown")


app = FastAPI(title="Check documents", lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/docs")
async def docs():
    return RedirectResponse(url="/docs")


@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile):
    file_path = f"storage/{file.filename}"
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    text = "\n".join(text)
    vector_store = VectorStore()
    db = vector_store.load_vectordb()
    docs = db.similarity_search(text, k=5)
    return templates.TemplateResponse("result.html",
                                      {"request": request,
                                       "content": "\n\n".join(doc.page_content for doc in docs),
                                       "filename": file.filename, })


@app.get("/", tags=["start_page"], response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/loader/", tags=["data_loader_2db"], response_class=HTMLResponse)
async def data_loader(request: Request):
    return templates.TemplateResponse("data_loader.html", {"request": request})


@app.post("/upload_2db/", response_class=JSONResponse)
async def upload_file_2db(file: UploadFile = File(...)):
    file_path = f"storage/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    splitter = Splitter(file_path)
    documents = splitter.process_files()
    vector_store = VectorStore()
    vector_store.add_2vectordb(documents)
    return {"filename": file.filename}

