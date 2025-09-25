import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# .env 로드
load_dotenv()

app = FastAPI(title="CXR.Web Backend", version="0.1.0")

# 환경변수 기반 origin
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 개발: localhost, 운영: 실제 도메인
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

