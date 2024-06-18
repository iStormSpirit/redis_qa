from fastapi import FastAPI
from src.api import endpoints
from src.worker import worker  # Import to start worker thread
from fastapi.responses import ORJSONResponse

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"displayRequestDuration": True},
)

app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
