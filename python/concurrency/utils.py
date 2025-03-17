import time
import asyncio
from functools import wraps
from typing import Any, Callable

def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} completed in {end - start:.2f} seconds")
        return result
    return wrapper

def async_timer(func: Callable, print_start=True, print_finish=True) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        if print_start:
            print(f"Starting {func.__name__}")
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        if print_finish:
            print(f"{func.__name__} completed in {end - start:.2f} seconds")
        return result
    return wrapper

def io_bound_task(name: str, seconds: float, willError: bool = False, print_start: bool = True, print_finish: bool = True) -> str:
    if print_start:
        print(f"Starting {name}")
    time.sleep(seconds)
    if willError:
        raise ValueError(f"{name} error")
    if print_finish:
        print(f"Finished {name}")
    return f"{name} result"

async def async_io_bound_task(name: str, seconds: float, willError: bool = False, print_start: bool = True, print_finish: bool = True) -> str:
    if print_start:
        print(f"Starting {name}")
    await asyncio.sleep(seconds)
    if willError:
        raise ValueError(f"{name} error")
    if print_finish:
        print(f"Finished {name}")
    return f"{name} result"

def cpu_bound_task(name: str, seconds: float, print_start: bool = True, print_finish: bool = True) -> int:
    if print_start:
        print(f"Starting {name}")
    time.sleep(seconds)
    if print_finish:
        print(f"Finished {name}")
    return f"{name} result"

def run_examples(*funcs: Callable) -> None:
    """Execute multiple functions with newlines between them.
    
    Args:
        *funcs: Variable number of functions to execute
    """
    for i, func in enumerate(funcs):
        if i > 0:
            print("\n")  # Add newline between functions
        func()