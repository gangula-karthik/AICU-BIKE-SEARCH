import sys
sys.path.append('./app')
from fastapi import FastAPI, UploadFile, Form, HTTPException, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.emojii_and_emoticon_map import EMOTICONS_EMO, EMOJI_UNICODE
from app.preprocess_data import *
from app.querying_data import process_and_query_text, process_and_query_image_url
from fastapi.middleware.cors import CORSMiddleware
import chromadb

app = FastAPI()

class TextRequest(BaseModel):
    text: str

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

def setup_chromadb():
    chroma_client = chromadb.PersistentClient(path="./data/AICU-VECTOR-DB")
    collection = chroma_client.get_collection(name="aicu-bike-search")
    return collection

@app.get("/")
async def root():
    return {"message": "Welcome to the AICU API! Go to /docs to see the API documentation."}

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    global collection, model, preprocess
    collection = setup_chromadb()
    model, preprocess, _, _, _, _ = load_clip_model(device='cpu')
    logger.info("ChromaDB collection initialized.")

async def prepare_image(file: UploadFile, preprocess):
    img_bytes = await file.read()
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    
    if img is not None:
        img_input = preprocess(img).unsqueeze(0)
        return img_input
    else:
        return None

@app.post("/process_image/")
async def process_image_and_query(file: UploadFile = File(...)):
    try:
        img_input = await prepare_image(file, preprocess)
        if img_input is not None:
            results = process_and_query_image_url(img_input, model, 'cpu', collection)
            print(results)
            return {"results": results}
        else:
            raise HTTPException(status_code=400, detail="Failed to process image.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/process_text/")
async def process_text(text):
    processed_text = remove_punct(text)
    processed_text = remove_emojis_and_emoticons(processed_text)
    processed_text = mask_all(processed_text)
    results = process_and_query_text(processed_text, model, 'cpu', collection)
    return {"results": results}