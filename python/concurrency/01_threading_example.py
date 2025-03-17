import threading
from utils import cpu_bound_task, timer, io_bound_task, run_examples
import time

@timer
def threading_without_waiting_for_the_result():
    print("=== Threading without waiting for the result ===")
    threads = []
    for i in range(5):
        thread = threading.Thread(
            target=io_bound_task, 
            args=(f"Task {i}", 1)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

@timer
def threading_waiting_for_the_result():
    print("=== Threading waiting for the result ===")
    threads = []
    results = [None] * 5
    
    def task_with_result(idx, name, delay):
        result = io_bound_task(name, delay)
        results[idx] = result
    
    for i in range(5):
        thread = threading.Thread(
            target=task_with_result,
            args=(i, f"Task {i}", 1)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Results from shared list: {results}")

@timer
def threading_waiting_for_the_result_when_an_error_occurs():
    print("=== Threading waiting for the result when an error occurs ===")
    threads = []
    results = [None] * 5
    
    def task_with_result(idx, name, delay):
        results[idx] = io_bound_task(name, delay, willError=idx==3)
    
    for i in range(5):
        thread = threading.Thread(
            target=task_with_result,
            args=(i, f"Task {i}", 1)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join() # Thread errors won't propagate here

    print(f"Results from shared list: {results}")

@timer
def threading_with_cancellation():
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

    threads = []
    for i in range(2):
        thread = threading.Thread(
            target=cancellable_task,
            args=(i, cancellation_token)
        )
        threads.append(thread)
        thread.start()

    time.sleep(3)
    cancellation_token.set()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    run_examples(
        # threading_without_waiting_for_the_result,
        # threading_waiting_for_the_result,
        # threading_waiting_for_the_result_when_an_error_occurs,
        threading_with_cancellation,
    ) 