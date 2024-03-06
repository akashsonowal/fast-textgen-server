from contextlib import asynccontextmanager
from typing import Callable, Optional

from fastapi import FastAPI, HTTPException
from uvicorn import run
from pydantic import BaseModel

from .batching import BatchProcessor
from .handler import BaseHandler, ParallelHandler
from .middleware import register_default_middlewares
from .utils import BaseRequest


class BaseServe:
    def __init__(
        self,
        handle: Callable,
        batch_size: int,
        timeout: float,
        auth_token: str,
        input_schema: Optional[BaseModel],
        response_schema: Optional[BaseModel],
    ) -> None:
        self.input_schema = input_schema
        self.auth_token = auth_token
        self.response_schema = response_schema
        self.handle = handle
        self.batch_processing = BatchProcessor(
            func=self.handle, bs=batch_size, timeout=timeout
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            self.batch_processing.cancel()

        self._app = FastAPI(lifespan=lifespan, title="ML Service", docs_url="/")
        register_default_middlewares(self._app)
        INPUT_SCHEMA = input_schema

        def api(request: INPUT_SCHEMA):
            if request.authtoken != self.auth_token:
                raise HTTPException(status_code=401, detail="Invalid auth token")
            print("incoming requests")
            wait_obj = self.batch_processing.process(request)
            result = wait_obj.get()
            return result

        self._app.add_api_route(
            path="/endpoint",
            endpoint=api,
            methods=["post"],
            response_model=response_schema,
        )

    @property
    def app(self):
        return self._app

    @property
    def run_server(self):
        run(self.app, host="0.0.0.0", port=8080)

    @property
    def test_client(self):
        from fastapi.testclient import TestClient

        return TestClient(self._app)


class LLMServe(BaseServe, BaseHandler):
    def __init__(
        self, batch_size=1, timeout=0.0, auth_token="79870be8ab3a7233e3ff8f636dec13e2", input_schema=None, response_schema=None
    ):
        if input_schema is None:
            input_schema = BaseRequest
        super().__init__(
            handle=self.handle,
            batch_size=batch_size,
            timeout=timeout,
            auth_token=auth_token,
            input_schema=input_schema,
            response_schema=response_schema,
        )


class ParallelLLMServe(BaseServe, ParallelHandler):
    def __init__(
        self, batch_size=1, timeout=0.0, auth_token="79870be8ab3a7233e3ff8f636dec13e2", input_schema=None, response_schema=None
    ):
        super().__init__(
            handle=self.handle,
            batch_size=batch_size,
            timeout=timeout,
            auth_token=auth_token,
            input_schema=input_schema,
            response_schema=response_schema,
        )