import os
import random
from abc import abstractmethod
from typing import List
from .utils import BaseRequest 

import uactor 

class BaseHandler:
    def create_model():
        raise NotImplementedError("You must implement create_model.")

    @abstractmethod
    def handle(self, batch: List[BaseRequest]):
        raise NotImplementedError("You must implement handle to run a server.")

class ParallelHandler(BaseHandler, uactor.Actor):
    """This is a Parallel Handler."""

class DummyHandler(BaseHandler):
    def create_model(self):
        self.model = lambda x: 1
    
    def handle(self, batch: List[BaseRequest]):
        print(f"Hello from subprocess {os.getpid()}!")
        return [random.randint(1, 10)] * len(batch)