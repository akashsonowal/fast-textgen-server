from llm_serve.app import BaseServe
from llm_serve.handler import DummyHandler
from llm_serve.utils import BaseRequest

handler = DummyHandler()
serve = BaseServe(
    handler=handler,
    bs=1,
    timeout=0,
    input_schema=BaseRequest,
)
serve.run_server() # running BaseServe (the core logic)