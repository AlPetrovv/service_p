from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from lifespan import lifespan
from presentation.http.error_handlers import setup_exception_handlers
from routers import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Service P",
        description="Async REST API for users, accounts and payment webhooks",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )

    @app.get("/health", tags=["Health"], summary="Health check")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_router)
    setup_exception_handlers(app)
    return app


main_app = create_app()

if __name__ == "__main__":
    import uvicorn

    # reload is for local development only.
    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)
