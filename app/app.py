from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from emojii_and_emoticon_map import EMOTICONS_EMO, EMOJI_UNICODE
from preprocess_data import *
from querying_data import process_and_query_text, process_and_query_image_url

app = FastAPI()


class ImageResponse(BaseModel):
    success: bool
    message: str
    data: Optional[str] = None

class TextResponse(BaseModel):
    success: bool
    message: str
    data: Optional[str] = None

@app.post("/process-image/", response_model=ImageResponse)
async def process_image_and_query(url: str):
    model, preprocess, _, _, _, _ = load_clip_model()
    img_input = prepare_image(url, preprocess)
    if img_input is not None:
        results = process_and_query_image_url(img_input, model, 'cuda', collection)  # Replace 'collection' with your collection object
        return ImageResponse(success=True, message="Image processed and queried successfully.", data=results)
    else:
        raise HTTPException(status_code=400, detail="Failed to process image.")
    
@app.post("/process-text/", response_model=TextResponse)
async def process_text_and_query(text: str):
    model, _, _, _, _, _ = load_clip_model()
    processed_text = remove_punct(text)
    processed_text = remove_emojis_and_emoticons(processed_text)
    processed_text = mask_all(processed_text)
    results = process_and_query_text(processed_text, model, 'cuda', collection)  # Replace 'collection' with your collection object
    return TextResponse(success=True, message="Text processed and queried successfully.", data=results)