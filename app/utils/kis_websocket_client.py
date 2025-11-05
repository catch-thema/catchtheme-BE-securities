import asyncio
import json
import logging
from typing import Optional, Callable, Dict, Any
from decimal import Decimal
import websockets
from websockets.client import WebSocketClientProtocol

from app.core.config import settings
from app.core.constants import KISWebSocketConfig
from app.schemas.index import IndexData

logger = logging.getLogger(__name__)


class KISWebSocketClient:

    def __init__(self):
        self.ws: Optional[WebSocketClientProtocol] = None
        self.app_key = settings.KIS_APP_KEY
        self.app_secret = settings.KIS_APP_SECRET
        self.is_connected = False
        self.is_running = False
        self.reconnect_attempts = 0
        self.message_handler: Optional[Callable[[IndexData], None]] = None

        self.index_codes = {
            KISWebSocketConfig.INDEX_CODE_KOSPI: "KOSPI",
            KISWebSocketConfig.INDEX_CODE_KOSDAQ: "KOSDAQ",
            KISWebSocketConfig.INDEX_CODE_NASDAQ: "NASDAQ",
            KISWebSocketConfig.INDEX_CODE_SP500: "SP500"
        }

    async def connect(self):
        try:
            self.ws = await websockets.connect(
                KISWebSocketConfig.WEBSOCKET_URL,
                ping_interval=KISWebSocketConfig.PING_INTERVAL
            )
            self.is_connected = True
            self.reconnect_attempts = 0
            logger.info("KIS WebSocket connected successfully")

            await self._authenticate()
            await self._subscribe_indices()

        except Exception as e:
            logger.error(f"Failed to connect to KIS WebSocket: {e}")
            self.is_connected = False
            raise

    async def _authenticate(self):
        auth_data = {
            "header": {
                "approval_key": self._generate_approval_key(),
                "custtype": "P",
                "tr_type": "1",
                "content-type": "utf-8"
            }
        }

        await self.ws.send(json.dumps(auth_data))
        logger.info("WebSocket authentication sent")

    def _generate_approval_key(self) -> str:
        return f"{self.app_key}:{self.app_secret}"

    async def _subscribe_indices(self):
        for index_code in self.index_codes.keys():
            tr_id = self._get_tr_id_for_index(index_code)

            subscribe_data = {
                "header": {
                    "approval_key": self._generate_approval_key(),
                    "custtype": "P",
                    "tr_type": "1",
                    "content-type": "utf-8"
                },
                "body": {
                    "input": {
                        "tr_id": tr_id,
                        "tr_key": index_code
                    }
                }
            }

            await self.ws.send(json.dumps(subscribe_data))
            logger.info(f"Subscribed to index: {self.index_codes[index_code]} ({index_code})")

    def _get_tr_id_for_index(self, index_code: str) -> str:
        if index_code in [KISWebSocketConfig.INDEX_CODE_KOSPI, KISWebSocketConfig.INDEX_CODE_KOSDAQ]:
            return KISWebSocketConfig.TR_ID_DOMESTIC_INDEX
        return KISWebSocketConfig.TR_ID_OVERSEAS_INDEX

    async def listen(self):
        self.is_running = True

        try:
            while self.is_running and self.is_connected:
                try:
                    message = await asyncio.wait_for(
                        self.ws.recv(),
                        timeout=60.0
                    )
                    await self._handle_message(message)

                except asyncio.TimeoutError:
                    logger.warning("WebSocket receive timeout, sending ping")
                    await self.ws.ping()

                except websockets.exceptions.ConnectionClosed:
                    logger.warning("WebSocket connection closed")
                    self.is_connected = False
                    await self._reconnect()

        except Exception as e:
            logger.error(f"Error in WebSocket listener: {e}")
            self.is_connected = False

    async def _handle_message(self, message: str):
        try:
            data = json.loads(message)

            if "body" not in data:
                return

            body = data.get("body", {})
            output = body.get("output", {})

            if not output:
                return

            index_code = output.get("tr_key", "")
            if index_code not in self.index_codes:
                return

            index_data = self._parse_index_data(index_code, output)

            if self.message_handler and index_data:
                await self.message_handler(index_data)

        except Exception as e:
            logger.error(f"Failed to handle WebSocket message: {e}")

    def _parse_index_data(self, index_code: str, data: Dict[str, Any]) -> Optional[IndexData]:
        try:
            current_price = Decimal(str(data.get("price", "0")))
            change_price = Decimal(str(data.get("change", "0")))
            change_rate = Decimal(str(data.get("rate", "0")))
            timestamp = data.get("time", "")

            return IndexData(
                code=index_code,
                name=self.index_codes[index_code],
                current_price=current_price,
                change_rate=change_rate,
                change_price=change_price,
                timestamp=timestamp
            )
        except Exception as e:
            logger.error(f"Failed to parse index data: {e}")
            return None

    async def _reconnect(self):
        if self.reconnect_attempts >= KISWebSocketConfig.MAX_RECONNECT_ATTEMPTS:
            logger.error("Max reconnection attempts reached")
            return

        self.reconnect_attempts += 1
        logger.info(f"Attempting to reconnect ({self.reconnect_attempts}/{KISWebSocketConfig.MAX_RECONNECT_ATTEMPTS})")

        await asyncio.sleep(KISWebSocketConfig.RECONNECT_DELAY)

        try:
            await self.connect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")

    def set_message_handler(self, handler: Callable[[IndexData], None]):
        self.message_handler = handler

    async def disconnect(self):
        self.is_running = False
        self.is_connected = False

        if self.ws:
            await self.ws.close()
            logger.info("KIS WebSocket disconnected")

    async def start(self):
        await self.connect()
        await self.listen()
