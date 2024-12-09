# Swahili Text-to-Speech API
A FastAPI-based REST API that provides text-to-speech (TTS) capabilities for Swahili text using fine-tuned Hugging Face models.

## Features
- Converts Swahili text to speech using two different models:
  - Benny model: `Benjamin-png/swahili-mms-tts-finetuned`
  - Briget model: `Benjamin-png/swahili-mms-tts-Briget_580_clips-finetuned`
- Automatic Swahili language detection
- CORS support for cross-origin requests
- Efficient model caching
- Returns audio in WAV format

## Prerequisites
```bash
pip install -r requirements.txt
```

## Running the Server
To start the server:
```bash
python tts_linkedin.py
```
The server will run on `http://0.0.0.0:8000`

## API Endpoints
### 1. Generate Speech using Benny Model
**Endpoint:** `POST /tts/benny`
**Request Body:**
```json
{
    "text": "Your Swahili text here"
}
```

### 2. Generate Speech using Briget Model
**Endpoint:** `POST /tts/briget`
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
curl -X POST "http://localhost:8000/tts/briget" \
     -H "Content-Type: application/json" \
     -d '{"text":"Kijana huyu ni msataarabu sana sana"}' \
     --output output.wav
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/tts/briget",
    json={"text": "Kijana huyu ni msataarabu sana sana"}
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

## Docker Support
You can also run the API using Docker:
```bash
# Build the Docker image
docker build -t swahili-tts .

# Run the container
docker run -d -p 8000:8000 swahili-tts
```
