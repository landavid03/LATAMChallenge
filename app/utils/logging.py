import logging
import sys
from app.config import settings

# Configure basic logging
logging_format = "%(levelname)s:     %(asctime)s - %(name)s - %(message)s"


def setup_logging():
    #Configure application logging
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format=logging_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set loggers for external libraries
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
        logging.getLogger(logger_name).handlers = []
        logging.getLogger(logger_name).propagate = True

    # Disable SQLAlchemy logging if not explicitly enabled
    if not settings.DB_ECHO_LOG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logging.getLogger("app")


# Create a logger instance for import
logger = setup_logging()
