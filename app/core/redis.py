from redis import asyncio as aioredis

from app.core.config import load_config


settings = load_config()


redis = aioredis.from_url(f"redis://{settings.api.redis_host}:{settings.api.redis_port}",)
