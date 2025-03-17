import asyncio
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from utils import io_bound_task, async_io_bound_task, cpu_bound_task, timer, async_timer

@async_timer
async def basic_comparison():
    print("\n=== Basic Event Loop Comparison ===")
    
    async def using_get_loop():
        loop = asyncio.get_event_loop()
        return await async_io_bound_task("Task with get_loop()", 1)
    
    await using_get_loop()

@timer
def thread_event_loop():
    print("\n=== Event Loop Per Thread ===")
    
    async def thread_task():
        await async_io_bound_task("Thread Task", 1)
    
    def run_loop_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(thread_task())
        loop.close()
    
    threads = [
        threading.Thread(target=run_loop_in_thread)
        for _ in range(5)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

@async_timer
async def nested_loops_example():
    print("\n=== Nested Event Loops (Demonstration Only) ===")
    
    async def inner_task():
        print("Inner task starting")
        await async_io_bound_task("Inner Task", 1)
        print("Inner task finished")
    
    print("Outer task starting")
    await inner_task()
    print("Outer task finished")

@timer
def process_event_loop():
    print("\n=== Event Loops in Different Processes ===")
    
    async def process_task(name):
        await async_io_bound_task(name, 1)
    
    def run_loop_in_process(name):
        asyncio.run(process_task(name))
    
    processes = [
        multiprocessing.Process(
            target=run_loop_in_process,
            args=(f"Process {i}",)
        )
        for i in range(5)
    ]
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()

@async_timer
async def event_loop_best_practices():
    print("\n=== Event Loop Best Practices ===")
    
    loop = asyncio.get_event_loop()
    
    tasks = [
        async_io_bound_task(f"Concurrent Task {i}", 1)
        for i in range(5)
    ]
    results = await asyncio.gather(*tasks)
    
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, cpu_bound_task, 1000000)

if __name__ == "__main__":
    print("Event Loop Examples and Rules:\n")
    print("Rule 1: One event loop per thread")
    print("Rule 2: Nested event loops are not allowed")
    print("Rule 3: Each process can have its own event loop")
    print("Rule 4: asyncio.run() is preferred for top-level code")
    print("\nRunning examples...")
    
    asyncio.run(basic_comparison())
    thread_event_loop()
    asyncio.run(nested_loops_example())
    process_event_loop()
    asyncio.run(event_loop_best_practices()) 