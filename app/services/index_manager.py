import asyncio
import logging
from typing import Dict, Set, Optional
from fastapi import WebSocket

from app.utils.kis_websocket_client import KISWebSocketClient
from app.schemas.index import IndexData
from app.db.session import SessionLocal
from app.repositories.market_index_repository import MarketIndexRepository

logger = logging.getLogger(__name__)


class IndexDataManager:
    _instance: Optional['IndexDataManager'] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.kis_client = KISWebSocketClient()
            self.latest_data: Dict[str, IndexData] = {}
            self.subscribers: Set[WebSocket] = set()
            self.is_running = False
            self.background_task: Optional[asyncio.Task] = None
            self.initialized = True

    async def start(self):
        async with self._lock:
            if self.is_running:
                return

            self.is_running = True
            self.kis_client.set_message_handler(self._on_index_update)

            self.background_task = asyncio.create_task(self.kis_client.start())
            logger.info("IndexDataManager started")

    async def stop(self):
        async with self._lock:
            if not self.is_running:
                return

            self.is_running = False
            await self.kis_client.disconnect()

            if self.background_task:
                self.background_task.cancel()
                try:
                    await self.background_task
                except asyncio.CancelledError:
                    pass

            logger.info("IndexDataManager stopped")

    async def _on_index_update(self, index_data: IndexData):
        self.latest_data[index_data.code] = index_data
        await self._save_to_db(index_data)
        await self._broadcast_to_subscribers(index_data)

    async def _save_to_db(self, index_data: IndexData):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._sync_save_to_db, index_data)
        except Exception as e:
            logger.error(f"Failed to save index data to DB: {e}")

    def _sync_save_to_db(self, index_data: IndexData):
        db = SessionLocal()
        try:
            repository = MarketIndexRepository(db)
            repository.upsert_index(index_data)
        finally:
            db.close()

    async def _broadcast_to_subscribers(self, index_data: IndexData):
        disconnected_clients = set()

        for subscriber in self.subscribers:
            try:
                await subscriber.send_json(index_data.model_dump())
            except Exception as e:
                logger.warning(f"Failed to send data to subscriber: {e}")
                disconnected_clients.add(subscriber)

        self.subscribers -= disconnected_clients

    async def add_subscriber(self, websocket: WebSocket):
        self.subscribers.add(websocket)
        logger.info(f"Subscriber added. Total subscribers: {len(self.subscribers)}")

        for index_data in self.latest_data.values():
            try:
                await websocket.send_json(index_data.model_dump())
            except Exception as e:
                logger.error(f"Failed to send initial data: {e}")

    async def remove_subscriber(self, websocket: WebSocket):
        self.subscribers.discard(websocket)
        logger.info(f"Subscriber removed. Total subscribers: {len(self.subscribers)}")

    def get_latest_data(self) -> Dict[str, IndexData]:
        return self.latest_data.copy()


_manager: Optional[IndexDataManager] = None

async def get_index_manager() -> IndexDataManager:
    global _manager
    if _manager is None:
        _manager = IndexDataManager()
        await _manager.start()
    return _manager
