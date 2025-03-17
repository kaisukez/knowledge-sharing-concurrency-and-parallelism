import asyncio
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from utils import io_bound_task, async_io_bound_task, cpu_bound_task, timer, async_timer

@async_timer
async def asyncio_with_threading():
    print("\n=== Mixing Asyncio with Threading ===")
    
    async def async_main():
        with ThreadPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            cpu_tasks = [
                loop.run_in_executor(executor, cpu_bound_task, 1000000)
                for _ in range(5)
            ]
            
            io_tasks = [
                async_io_bound_task(f"IO Task {i}", 1)
                for i in range(5)
            ]
            
            all_tasks = cpu_tasks + io_tasks
            results = await asyncio.gather(*all_tasks)
            print(f"Results: {results}")
    
    await async_main()

@async_timer
async def asyncio_with_multiprocessing():
    print("\n=== Mixing Asyncio with Multiprocessing ===")
    
    async def async_main():
        with ProcessPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            cpu_tasks = [
                loop.run_in_executor(executor, cpu_bound_task, 1000000)
                for _ in range(5)
            ]
            
            io_tasks = [
                async_io_bound_task(f"IO Task {i}", 1)
                for i in range(5)
            ]
            
            all_tasks = cpu_tasks + io_tasks
            results = await asyncio.gather(*all_tasks)
            print(f"Results: {results}")
    
    await async_main()

@timer
def threading_with_multiprocessing():
    print("\n=== Mixing Threading with Multiprocessing ===")
    
    with ThreadPoolExecutor(max_workers=5) as thread_executor:
        with ProcessPoolExecutor(max_workers=5) as process_executor:
            io_futures = [
                thread_executor.submit(io_bound_task, f"IO Task {i}", 1)
                for i in range(5)
            ]
            
            cpu_futures = [
                process_executor.submit(cpu_bound_task, 1000000)
                for _ in range(5)
            ]
            
            all_futures = io_futures + cpu_futures
            results = [f.result() for f in all_futures]
            print(f"Results: {results}")

if __name__ == "__main__":
    print("Demonstrating Mixed Concurrency Approaches")
    
    asyncio.run(asyncio_with_threading())
    asyncio.run(asyncio_with_multiprocessing())
    threading_with_multiprocessing() 