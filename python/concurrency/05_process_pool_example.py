from concurrent.futures import ProcessPoolExecutor
from utils import timer, cpu_bound_task, run_examples
import time
import multiprocessing

def task_that_might_fail(idx, name, delay):
    if idx == 3:
        raise ValueError(f"Task {idx} failed!")
    return cpu_bound_task(name, delay)

def task_that_might_fail_with_exception_aggregation(idx, name, delay):
    try:
        return cpu_bound_task(name, delay, willError=idx==3)
    except ValueError as e:
        return e

def cancellable_task(process_number, shared_dict):
    if shared_dict['should_cancel']:
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 1", 1, print_start=False)

    if shared_dict['should_cancel']:
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 2", 1, print_start=False)

    if shared_dict['should_cancel']:
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 3", 1, print_start=False)

    if shared_dict['should_cancel']:
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 4", 1, print_start=False)

    if shared_dict['should_cancel']:
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 5", 1, print_start=False)

@timer
def process_pool_without_waiting_for_the_result():
    print("=== ProcessPool without waiting for the result ===")
    with ProcessPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit(cpu_bound_task, f"Task {i}", 1)

@timer
def process_pool_waiting_for_the_result():
    print("=== ProcessPool waiting for the result ===")
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(cpu_bound_task, f"Task {i}", 1)
            for i in range(5)
        ]
        results = [f.result() for f in futures]
        print(f"Results from futures list: {results}")

@timer
def process_pool_waiting_for_the_result_when_an_error_occurs():
    print("=== ProcessPool waiting for the result when an error occurs ===")
    
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(task_that_might_fail, i, f"Task {i}", 1)
            for i in range(5)
        ]
        
        results = [f.result() for f in futures]  # Error propagates to the main thread
        
        print(f"Results from futures list: {results}")

@timer
def process_pool_waiting_for_the_result_exception_aggregation():
    print("=== ProcessPool waiting for the result exception aggregation ===")
    
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(task_that_might_fail_with_exception_aggregation, i, f"Task {i}", 1)
            for i in range(5)
        ]
        
        results = [f.result() for f in futures]
        
        print(f"Results from futures list: {results}")

@timer
def process_pool_with_cancellation():
    print("=== ProcessPool with cancellation ===")
    with multiprocessing.Manager() as manager:
        shared_dict = manager.dict()
        shared_dict['should_cancel'] = False
        
        with ProcessPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(cancellable_task, i, shared_dict)
                for i in range(2)
            ]
            
            time.sleep(3)
            print("Cancelling tasks...")
            shared_dict['should_cancel'] = True
            
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Task cancelled or failed: {e}")

if __name__ == "__main__":
    run_examples(
        # process_pool_without_waiting_for_the_result,
        # process_pool_waiting_for_the_result,
        # process_pool_waiting_for_the_result_when_an_error_occurs,
        # process_pool_waiting_for_the_result_exception_aggregation,
        process_pool_with_cancellation
    ) 