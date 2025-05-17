from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging
logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_LOG,
    pool_pre_ping=True
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    logger.debug("Database session started")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")


def create_tables():
    #Create all tables in the database
    try:
        from app.schemas.users import User

        logger.info("Creating database tables")
        Base.metadata.create_all(bind=engine)
        print("Tablas en metadata:", Base.metadata.tables.keys())
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
