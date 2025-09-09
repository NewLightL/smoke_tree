from fastapi import APIRouter


router = APIRouter(prefix="/health")


@router.head("/")
async def head_health_check():
    """Простой endpoint для проверки работы"""
    return {"status": "ok", "message": "Server is alive"}


@router.get("/")
async def get_health_check():
    """Простой endpoint для проверки работы"""
    return {"status": "ok", "message": "Server is alive"}
