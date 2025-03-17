from concurrent.futures import ThreadPoolExecutor
from utils import cpu_bound_task, timer, io_bound_task, run_examples
import threading
import time

@timer
def thread_pool_without_waiting_for_the_result_without_context_manager():
    print("=== ThreadPool without waiting for the result without context manager ===")
    executor = ThreadPoolExecutor(max_workers=5)
    for i in range(5):
        executor.submit(io_bound_task, f"Task {i}", 1)
    executor.shutdown(wait=True) # Works like thread.join()

@timer
def thread_pool_without_waiting_for_the_result():
    print("=== ThreadPool without waiting for the result ===")
    # If we use Context Manager, then we don't need executor.shutdown(wait=True) like in the previous example
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit(io_bound_task, f"Task {i}", 1)

@timer
def thread_pool_waiting_for_the_result():
    print("=== ThreadPool waiting for the result ===")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(io_bound_task, f"Task {i}", 1)
            for i in range(5)
        ]
        results = [f.result() for f in futures]
        print(f"Results from futures list: {results}")

@timer
def thread_pool_waiting_for_the_result_when_an_error_occurs():
    print("=== ThreadPool waiting for the result when an error occurs ===")
    
    def task_that_might_fail(idx, name, delay):
        return io_bound_task(name, delay, willError=idx==3)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(task_that_might_fail, i, f"Task {i}", 1)
            for i in range(5)
        ]
        
        results = [f.result() for f in futures] # Error propagates to the main thread, need to catch it
        
        print(f"Results from futures list: {results}")

@timer
def thread_pool_waiting_for_the_result_exception_aggregation():
    print("=== ThreadPool waiting for the result exception aggregation ===")
    
    def task_that_might_fail(idx, name, delay):
        try:
            return io_bound_task(name, delay, willError=idx==3)
        except ValueError as e:
            return e
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(task_that_might_fail, i, f"Task {i}", 1)
            for i in range(5)
        ]
        
        results = [f.result() for f in futures]
        
        print(f"Results from futures list: {results}")

@timer
def thread_pool_with_cancellation():
    print("=== ThreadPool with cancellation ===")
    cancellation_token = threading.Event()

    def cancellable_task(thread_number, cancellation_token):
        if cancellation_token.is_set():
            print(f"Cancelled Thread {thread_number}")
            return
        io_bound_task(f"Thread {thread_number} -- Task 1", 1, print_start=False)

        if cancellation_token.is_set():
            print(f"Cancelled Thread {thread_number}")
            return
        io_bound_task(f"Thread {thread_number} -- Task 2", 1, print_start=False)

        if cancellation_token.is_set():
            print(f"Cancelled Thread {thread_number}")
            return
        cpu_bound_task(f"Thread {thread_number} -- Task 3", 1, print_start=False)

        if cancellation_token.is_set():
            print(f"Cancelled Thread {thread_number}")
            return
        cpu_bound_task(f"Thread {thread_number} -- Task 4", 1, print_start=False)

        if cancellation_token.is_set():
            print(f"Cancelled Thread {thread_number}")
            return
        io_bound_task(f"Thread {thread_number} -- Task 5", 1, print_start=False)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(cancellable_task, i, cancellation_token)
            for i in range(2)
        ]
        
        time.sleep(3)
        cancellation_token.set()
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    run_examples(
        # thread_pool_without_waiting_for_the_result,
        # thread_pool_waiting_for_the_result,
        # thread_pool_waiting_for_the_result_when_an_error_occurs,
        # thread_pool_waiting_for_the_result_exception_aggregation,
        thread_pool_with_cancellation,
    )