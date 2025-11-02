from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
import time

from backend.model import analyze_mood

from safety import is_crisis
from response_bank import empathetic_reply, crisis_reply

app = FastAPI(title="Mental Health Chatbot", version="0.1.0")

# CORS for the simple web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["endpoint", "method", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint", "method"])

class ChatInput(BaseModel):
    text: str

class ChatOutput(BaseModel):
    response: str
    mood: str
    crisis: bool

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/chat", response_model=ChatOutput)
def chat(inp: ChatInput):
    start = time.time()
    endpoint = "/chat"
    method = "POST"
    try:
        text = (inp.text or "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="Empty text")

        crisis = is_crisis(text)
        if crisis:
            response = crisis_reply()
            mood = "critical"
        else:
            mood = analyze_mood(text)  # "positive" | "neutral" | "negative"
            response = empathetic_reply(mood, user_text=text)

        return {"response": response, "mood": mood, "crisis": crisis}
    except HTTPException as e:
        REQUESTS.labels(endpoint=endpoint, method=method, status=e.status_code).inc()
        raise
    except Exception as e:
        REQUESTS.labels(endpoint=endpoint, method=method, status=500).inc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        LATENCY.labels(endpoint=endpoint, method=method).observe(time.time() - start)
        REQUESTS.labels(endpoint=endpoint, method=method, status=200).inc()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
