import requests
from PIL import Image
from io import BytesIO
import clip
import numpy as np
import logging
import re
from emojii_and_emoticon_map import EMOTICONS_EMO, EMOJI_UNICODE
import string


# FUNCTIONS TO LOAD THE CLIP MODEL
def load_clip_model(device):
    '''Load the CLIP model and return the model, utils and params.'''
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    if device == 'cuda' and not clip.available():
        logger.warning("CUDA is selected but not available. Switching to CPU.")
        device = 'cpu'
    
    model, preprocess = clip.load("ViT-B/32")
    model = model.to(device).eval()
    
    input_resolution = model.visual.input_resolution
    context_length = model.context_length
    vocab_size = model.vocab_size
    
    model_parameters = np.sum([int(np.prod(p.shape)) for p in model.parameters()])
    
    logger.info("Model parameters: %s", f"{model_parameters:,}")
    logger.info("Input resolution: %s", input_resolution)
    logger.info("Context length: %s", context_length)
    logger.info("Vocab size: %s", vocab_size)
    
    return model, preprocess, input_resolution, context_length, vocab_size, model_parameters


# THESE ARE THE FUNCTIONS FOR TEXT PREPROCESSING
EMOTICONS_PATTERN = '|'.join(map(re.escape, EMOTICONS_EMO.keys()))
EMOJIS_PATTERN = '|'.join(map(re.escape, EMOJI_UNICODE.values()))
COMBINED_PATTERN = f"(?:{EMOTICONS_PATTERN})|(?:{EMOJIS_PATTERN})"
PATTERN = re.compile(COMBINED_PATTERN)

def remove_emojis_and_emoticons(text):
    return PATTERN.sub('', text)

def remove_punct(text):
    text = re.sub(r'\*\*|\n', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def mask_all(text):
    combined_pattern = r'(?:\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)|' + \
                       r'(?:\+65\s?)?(?:\d{4}\s?\d{4})|' + \
                       r'(?:https?:\/\/www\.|https?:\/\/|www\.)[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}(\/\S*)?'
    
    masked_text = re.sub(combined_pattern, lambda x: '[email_masked]' if '@' in x.group(0) else 
                         ('[phone_masked]' if x.group(0).replace(' ', '').isdigit() or '+65' in x.group(0) else '[website_masked]'), text)
    
    return masked_text

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


# FUNCTIONS TO PREPARE THE IMAGE
def url_to_img(url):
    '''Load an image from a URL and return it as a PIL image.'''
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img

def prepare_image(url, preprocess):
    img = url_to_img(url)
    if img is not None:
        img_input = preprocess(img).unsqueeze(0)
        return img_input
    else:
        return None