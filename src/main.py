import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import endpoints
# from multiprocessing import Process
# from src.worker.worker import start_workers

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"displayRequestDuration": True},
)

app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # fastapi_process = Process(target=uvicorn.run, args=(app,), kwargs={"host": "0.0.0.0", "port": 8000})
    # fastapi_process.start()
    #
    # start_workers()
    # fastapi_process.join()
    #
    # worker_process = Process(target=start_workers)
    # worker_process.start()
    #
    # fastapi_process.join()
    # worker_process.join()
