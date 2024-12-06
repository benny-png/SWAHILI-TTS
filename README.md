# Swahili Text-to-Speech API

A FastAPI-based REST API that provides text-to-speech (TTS) capabilities for Swahili text using both fine-tuned and original MMS-TTS models.

## Features

- Converts Swahili text to speech using two different models:
  - Fine-tuned model based on `Benjamin-png/swahili-mms-tts-finetuned`
  - Original model from `facebook/mms-tts-swh`
- Automatic Swahili language detection
- CORS support for cross-origin requests
- Efficient model caching
- Returns audio in WAV format

## Prerequisites

```bash
pip install fastapi uvicorn transformers torch numpy scipy langdetect
```

## Running the Server

To start the server:

```bash
python main.py
```

The server will run on `http://0.0.0.0:8000`

## API Endpoints

### 1. Generate Speech using Fine-tuned Model

**Endpoint:** `POST /tts/finetuned`

**Request Body:**
```json
{
    "text": "Your Swahili text here"
}
```

### 2. Generate Speech using Original Model

**Endpoint:** `POST /tts/original`

**Request Body:**
```json
{
    "text": "Your Swahili text here"
}
```

### Response

Both endpoints return:
- Content-Type: `audio/wav`
- Binary audio data in WAV format

### Error Responses

- `400 Bad Request`: If the provided text is not in Swahili
- Standard HTTP error codes for other failure cases

## Example Usage

Using curl:
```bash
curl -X POST "http://localhost:8000/tts/finetuned" \
     -H "Content-Type: application/json" \
     -d '{"text":"Habari yako"}' \
     --output output.wav
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/tts/finetuned",
    json={"text": "Habari yako"}
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

## Technical Details

- Uses PyTorch for model inference
- Models are automatically loaded on first use and cached
- Runs on GPU if available, falls back to CPU
- Audio is generated at the model's native sampling rate
- Output is converted to 16-bit PCM WAV format

## Implementation Notes

- The API uses `lru_cache` for efficient model loading
- Language detection is performed using the `langdetect` library
- CORS is configured to allow all origins, methods, and headers
- Audio processing uses scipy for WAV file generation
- The server uses FastAPI's automatic request validation with Pydantic models

