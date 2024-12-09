from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, VitsModel
import torch
import numpy as np
import io
from fastapi.responses import StreamingResponse
import scipy.io.wavfile
from langdetect import detect, LangDetectException
from functools import lru_cache
from dotenv import load_dotenv

app = FastAPI()


# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use lru_cache to cache model loading
@lru_cache()
def load_model(model_name):
    device = "cpu"
    model = VitsModel.from_pretrained(model_name, token=HF_TOKEN).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
    return model, tokenizer, device

# Load models and tokenizers
finetuned_model_name = "Benjamin-png/swahili-mms-tts-finetuned"
original_model_name = "Benjamin-png/swahili-mms-tts-Briget_580_clips-finetuned"

class TTSRequest(BaseModel):
    text: str

def is_swahili(text: str) -> bool:
    try:
        return detect(text) == 'sw'
    except LangDetectException:
        return False

def generate_audio(text: str, model_name):
    model, tokenizer, device = load_model(model_name)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model(**inputs).waveform
    output_np = output.squeeze().cpu().numpy()
    return output_np, model.config.sampling_rate

@app.post("/tts/benny")
async def tts_finetuned(request: TTSRequest):
    if not is_swahili(request.text):
        raise HTTPException(status_code=400, detail="The provided text is not in Swahili.")
    
    audio, sample_rate = generate_audio(request.text, finetuned_model_name)
    
    # Convert to WAV format
    bytes_io = io.BytesIO()
    scipy.io.wavfile.write(bytes_io, sample_rate, (audio * 32767).astype(np.int16))
    bytes_io.seek(0)
    
    return StreamingResponse(bytes_io, media_type="audio/wav")

@app.post("/tts/briget")
async def tts_original(request: TTSRequest):
    if not is_swahili(request.text):
        raise HTTPException(status_code=400, detail="The provided text is not in Swahili.")
    
    audio, sample_rate = generate_audio(request.text, original_model_name)
    
    # Convert to WAV format
    bytes_io = io.BytesIO()
    scipy.io.wavfile.write(bytes_io, sample_rate, (audio * 32767).astype(np.int16))
    bytes_io.seek(0)
    
    return StreamingResponse(bytes_io, media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
