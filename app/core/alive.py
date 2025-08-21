import logging

import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


logger = logging.getLogger(__name__)


class KeepAlive:
    def __init__(self, url: str):
        self.url = url
        self.scheduler = BackgroundScheduler()
        self.interval = IntervalTrigger(minutes=10)
        
    def start(self):
        """Запускает периодические запросы"""
        self.scheduler.add_job(
            self.ping_server,
            self.interval,
            id='keep_alive',
            name='Ping server every 10 min'
        )
        self.scheduler.start()
        logger.info("Keep-alive scheduler started")

    def ping_server(self):
        """Отправляет запрос для поддержания активности"""
        try:
            response = httpx.get(f"{self.url}/health", timeout=10)
            logger.info(f"Keep-alive ping: {response.status_code}")
        except Exception as e:
            logger.error(f"Keep-alive failed: {e}")

    def stop(self):
        """Останавливает scheduler"""
        self.scheduler.shutdown()
        logger.info("Keep-alive scheduler stopped")
