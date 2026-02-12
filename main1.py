from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import ocr
app = FastAPI(
    title="Prescription Analyzer API",
    description="Upload prescription image → OCR → Gemini → Structured JSON",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze/", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):

    image_bytes = await file.read()
    result = ocr.prescription(image_bytes)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result
        }
    )