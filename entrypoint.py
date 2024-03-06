from src.llm_serve.model import ServeLLama2 

serve = ServeLLama2(batch_size=2, timeout=1, auth_token="79870be8ab3a7233e3ff8f636dec13e2")
serve.run_server()