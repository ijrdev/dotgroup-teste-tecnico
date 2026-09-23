import time, logging

from functools import wraps

def sync_retry_decorator(attempts: int, delay: int, exceptions: set):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            turns: int = 0
            
            while turns < attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    turns += 1
                    
                    logging.warning(f"Attempts {turns}: {func.__name__}.")
                    
                    if turns == attempts:
                        raise
                    
                    time.sleep(delay)
        return wrapper
    return decorator

def async_retry_decorator(attempts: int, delay: int, exceptions: set):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            turns: int = 0
            
            while turns < attempts:
                try:
                    return await func(*args, **kwargs)
                except exceptions:
                    turns += 1
                    
                    logging.warning(f"Attempts {turns}: {func.__name__}.")
                    
                    if turns == attempts:
                        raise
                    
                    time.sleep(delay)
        return wrapper
    return decorator
