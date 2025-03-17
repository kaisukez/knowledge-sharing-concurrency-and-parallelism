import asyncio
from concurrent.futures import ProcessPoolExecutor
from utils import cpu_bound_task, timer, async_io_bound_task, run_examples, io_bound_task

@timer
def asyncio_convert_blocking_to_non_blocking_when_working_with_legacy_library():
    print("=== Asyncio convert blocking to non-blocking when working with legacy library ===")
    async def main():
        result = await asyncio.to_thread(io_bound_task, f"IO Bound Task, but blocking, because it's a legacy library", 1)
        print("Result: " + result)
    asyncio.run(main())

@timer
def asyncio_with_processes():
    print("=== Asyncio with processes ===")
    async def main():
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor() as pool:
            results = await asyncio.gather(
                loop.run_in_executor(pool, cpu_bound_task, "Compute 3 seconds", 3),
                loop.run_in_executor(pool, cpu_bound_task, "Compute 5 seconds", 5)
            )
            for result in results:
                print(f"Process result: {result}")
    asyncio.run(main())

if __name__ == "__main__":
    run_examples(
        # asyncio_convert_blocking_to_non_blocking_when_working_with_legacy_library,
        asyncio_with_processes,
    )