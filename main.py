# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

DEEPGRAM_API_KEY = "74475e9c588b9bf0ed9f2fac024959f044c9ebf2"  # ⬅️ paste your real key here

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def transcribe_audio(audio_file: UploadFile) -> str:
    async with httpx.AsyncClient() as client:
        audio_bytes = await audio_file.read()

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }

        response = await client.post(
            "https://api.deepgram.com/v1/listen",
            headers=headers,
            content=audio_bytes
        )

        data = response.json()
        transcript = data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
        return transcript

@app.post("/analyze")
async def analyze_audio(audio: UploadFile = File(...)):
    transcript = await transcribe_audio(audio)

    # Dummy AI feedback (for now)
    feedback = "Great start! Here's a tip: avoid filler words like 'uh' and 'um'."

    return {
        "transcript": transcript,
        "feedback": feedback
    }
