import asyncio
from utils import cpu_bound_task, timer, async_io_bound_task, run_examples

@timer
def asyncio_without_waiting_for_the_result():
    print("=== Asyncio without waiting for the result ===")
    async def main():
        for i in range(5):
            # Create but don't await the task
            asyncio.create_task(async_io_bound_task(f"Task {i}", 1))
        # Need to sleep a bit to let tasks complete since we're not awaiting them
        await asyncio.sleep(2)
    
    asyncio.run(main())

@timer
def asyncio_waiting_for_the_result():
    print("=== Asyncio waiting for the result ===")
    async def main():
        tasks = [
            async_io_bound_task(f"Task {i}", 1)
            for i in range(5)
        ]
        results = await asyncio.gather(*tasks)
        print(f"Results from tasks list: {results}")
    
    asyncio.run(main())

@timer
def asyncio_waiting_for_the_result_when_an_error_occurs():
    print("=== Asyncio waiting for the result when an error occurs ===")
    
    async def task_that_might_fail(idx, name, delay):
        if idx == 3:
            raise ValueError(f"Task {idx} failed!")
        return await async_io_bound_task(name, delay)
    
    async def main():
        tasks = [
            task_that_might_fail(i, f"Task {i}", 1)
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks) # Errors propagate to the main thread, need to catch it

        print(f"Results from tasks list: {results}")
    
    asyncio.run(main())

@timer
def asyncio_waiting_for_the_result_exception_aggregation():
    print("=== Asyncio waiting for the result exception aggregation ===")
    
    async def task_that_might_fail(idx, name, delay):
        return await async_io_bound_task(name, delay, willError=idx==3)
    
    async def main():
        tasks = [
            task_that_might_fail(i, f"Task {i}", 1)
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)

        print(f"Results from tasks list: {results}")
    
    asyncio.run(main())

@timer
def asyncio_with_cancellation():
    print("=== Asyncio with cancellation ===")
    
    async def cancellable_task(task_number):
        try:
            await async_io_bound_task(f"Task {task_number} -- Step 1", 1, print_start=False)

            await async_io_bound_task(f"Task {task_number} -- Step 2", 1, print_start=False)

            await asyncio.sleep(0.00001) # adding checkpoint to check if the task is cancelled
            cpu_bound_task(f"Task {task_number} -- Step 3", 1, print_start=False)

            await asyncio.to_thread(cpu_bound_task, f"Task {task_number} -- Step 4", 1, print_start=False)

            await async_io_bound_task(f"Task {task_number} -- Step 5", 1, print_start=False)
        except asyncio.CancelledError:
            print(f"Cancelled Task {task_number}")
            raise  # Re-raise to properly handle cancellation
    
    async def main():
        # Create tasks
        tasks = [
            asyncio.create_task(cancellable_task(i))
            for i in range(2)
        ]
        
        await asyncio.sleep(3)
        for task in tasks:
            task.cancel()
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("Tasks were cancelled")
    
    asyncio.run(main())

if __name__ == "__main__":
    run_examples(
        # asyncio_without_waiting_for_the_result,
        # asyncio_waiting_for_the_result,
        # asyncio_waiting_for_the_result_when_an_error_occurs,
        # asyncio_waiting_for_the_result_exception_aggregation,
        asyncio_with_cancellation,
    ) 