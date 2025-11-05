from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import logging

from app.services.index_manager import get_index_manager
from app.core.constants import Message
from app.db.session import get_db
from app.repositories.market_index_repository import MarketIndexRepository
from app.schemas.index import IndexData

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/indices/realtime")
async def websocket_realtime_indices(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected")

    manager = await get_index_manager()

    try:
        await websocket.send_json({
            "type": "connection",
            "message": Message.WEBSOCKET_CONNECTED
        })

        await manager.add_subscriber(websocket)

        while True:
            data = await websocket.receive_text()

            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        await manager.remove_subscriber(websocket)


@router.get("/indices/latest")
async def get_latest_indices(db: Session = Depends(get_db)):
    manager = await get_index_manager()
    latest_data = manager.get_latest_data()

    if not latest_data:
        logger.info("No real-time data available, fetching from DB")
        repository = MarketIndexRepository(db)
        db_indices = repository.get_all_indices()

        latest_data = {
            code: IndexData(
                code=index.code,
                name=index.name,
                current_price=index.current_price,
                change_rate=index.change_rate,
                change_price=index.change_price,
                timestamp=index.timestamp
            )
            for code, index in db_indices.items()
        }

    return {
        "status": 200,
        "message": "최신 지수 데이터 조회 성공",
        "data": {
            "indices": [data.model_dump() for data in latest_data.values()]
        }
    }
