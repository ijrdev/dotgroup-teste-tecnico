from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

class RateLimit():
    instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(RateLimit, cls).__new__(cls)
            
        return cls.instance
    
    limiter: Limiter = Limiter(key_func = get_remote_address)

    def __init__(self) -> FastAPI:
        try:
            self.limiter: Limiter = Limiter(key_func = get_remote_address)
        except Exception as ex:
            raise
