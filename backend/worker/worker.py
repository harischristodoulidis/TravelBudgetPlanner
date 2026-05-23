import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def run():
    logger.info("Worker started")
    while True:
        logger.info("Worker heartbeat at %s", datetime.now().isoformat())
        time.sleep(5)


if __name__ == "__main__":
    run()
