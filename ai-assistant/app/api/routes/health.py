from fastapi import APIRouter, HTTPException
from app.db.database import get_connection

router = APIRouter()

@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/db")
def database_health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1").fetchone()

        return {"status": "ok", "database": "connected"}

    except Exception:
        raise HTTPException(status_code=500, detail="Database connection failed")