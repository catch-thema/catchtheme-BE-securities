import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.repositories.exchange_rate_repository import ExchangeRateRepository

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def update_exchange_rate_job():
    db = SessionLocal()
    try:
        repository = ExchangeRateRepository()
        result = repository.update_usd_exchange_rate(db)

        if result:
            logger.info(f"Exchange rate updated successfully: USD/KRW = {result.base_rate}")
        else:
            logger.warning("Failed to update exchange rate")
    except Exception as e:
        logger.error(f"Error in exchange rate update job: {str(e)}")
    finally:
        db.close()

def start_scheduler():
    logger.info("Starting exchange rate scheduler...")

    update_exchange_rate_job()

    scheduler.add_job(
        update_exchange_rate_job,
        'interval',
        minutes=3,
        id='update_exchange_rate',
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
    logger.info("Exchange rate scheduler started (polling every 3 minutes)")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Exchange rate scheduler stopped")
