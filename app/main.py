from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.api.routes import users
from app.config import settings
from app.client.database import create_tables
from app.utils.logging import logger

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Process the request
    response = await call_next(request)

    # Log the request
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Process Time: {process_time:.4f}s"
    )

    return response


# Include API routes
app.include_router(users.router, prefix=settings.API_V1_STR)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.on_event("startup")
def startup_event():
    """Run actions on application startup"""
    logger.info("Starting User Management API Here")
    create_tables()


@app.on_event("shutdown")
def shutdown_event():
    """Run actions on application shutdown"""
    logger.info("Shutting down User Management API")


@app.get("/")
def root():
    """Root endpoint - redirects to documentation"""
    return {"message": f"User Management API - See documentation at {settings.API_V1_STR}/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
