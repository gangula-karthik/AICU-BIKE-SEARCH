from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from emojii_and_emoticon_map import EMOTICONS_EMO, EMOJI_UNICODE
from preprocess_data import *
from querying_data import process_and_query_text, process_and_query_image_url
import chromadb

app = FastAPI()

class ImageResponse(BaseModel):
    success: bool
    message: str
    data: Optional[str] = None

class TextResponse(BaseModel):
    success: bool
    message: str
    data: Optional[str] = None


def setup_chromadb():
    chroma_client = chromadb.PersistentClient(path="../data/AICU-VECTOR-DB")
    collection = chroma_client.get_collection(name="aicu-bike-search")
    return collection

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    global collection, model, preprocess
    collection = setup_chromadb()
    model, preprocess, _, _, _, _ = load_clip_model(device='cpu')
    logger.info("ChromaDB collection initialized.")

@app.post("/process_image/")
async def process_image_and_query(url: str):
    img_input = prepare_image(url, preprocess)
    if img_input is not None:
        results = process_and_query_image_url(img_input, model, 'cpu', collection)
        return {"results": results}
    else:
        raise HTTPException(status_code=400, detail="Failed to process image.")
    
@app.post("/process_text/")
async def process_text(text: str):
    processed_text = remove_punct(text)
    processed_text = remove_emojis_and_emoticons(processed_text)
    processed_text = mask_all(processed_text)
    results = process_and_query_text(processed_text, model, 'cpu', collection)
    return {"results": results}