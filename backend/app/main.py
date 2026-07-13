from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.extraction import router as extraction_router
from app.routers.documents import router as documents_router

app = FastAPI(
    title="File Parsing API",
    version="1.0.0"
)

# Allowed Frontend Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",

    # Vercel Frontend
    "https://file-parshing.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(extraction_router)
app.include_router(documents_router)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Backend Running Successfully"
    }