from fastapi import APIRouter


router = APIRouter(prefix="/health")


@router.get("/")
async def health_check():
    """Простой endpoint для проверки работы"""
    return {"status": "ok", "message": "Server is alive"}
