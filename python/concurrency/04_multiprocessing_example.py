import multiprocessing
from utils import timer, cpu_bound_task, run_examples
import time

def task_with_result(idx, name, delay, results):
    result = cpu_bound_task(name, delay)
    results[idx] = result

def task_with_result_with_error(idx, name, delay, results):
    if idx == 3:
        raise ValueError(f"Task {idx} failed!")
    results[idx] = cpu_bound_task(name, delay)

def cancellable_task(process_number, cancellation_token):
    if cancellation_token.is_set():
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 1", 1, print_start=False)

    if cancellation_token.is_set():
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 2", 1, print_start=False)

    if cancellation_token.is_set():
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 3", 1, print_start=False)

    if cancellation_token.is_set():
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 4", 1, print_start=False)

    if cancellation_token.is_set():
        print(f"Cancelled Process {process_number}")
        return
    cpu_bound_task(f"Process {process_number} -- Task 5", 1, print_start=False)

@timer
def multiprocessing_without_waiting_for_the_result():
    print("=== Multiprocessing without waiting for the result ===")
    processes = []
    for i in range(5):
        process = multiprocessing.Process(
            target=cpu_bound_task,
            args=(f"Task {i}", 1)
        )
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

@timer
def multiprocessing_waiting_for_the_result():
    print("=== Multiprocessing waiting for the result ===")
    processes = []
    with multiprocessing.Manager() as manager:
        results = manager.list([None] * 5)  # Need to declare shared variable this way
        
        for i in range(5):
            process = multiprocessing.Process(
                target=task_with_result,
                args=(i, f"Task {i}", 1, results)
            )
            processes.append(process)
            process.start()
        
        for process in processes:
            process.join()
        
        print(f"Results from shared list: {list(results)}")

@timer
def multiprocessing_waiting_for_the_result_when_an_error_occurs():
    print("=== Multiprocessing waiting for the result when an error occurs ===")
    processes = []
    with multiprocessing.Manager() as manager:
        results = manager.list([None] * 5)
        
        for i in range(5):
            process = multiprocessing.Process(
                target=task_with_result_with_error,
                args=(i, f"Task {i}", 1, results)
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()  # Process errors won't propagate here

        print(f"Results from shared list: {list(results)}")

@timer
def multiprocessing_with_cancellation():
    print("=== Multiprocessing with cancellation ===")
    processes = []
    cancellation_token = multiprocessing.Event()

    for i in range(2):
        process = multiprocessing.Process(
            target=cancellable_task,
            args=(i, cancellation_token)
        )
        processes.append(process)
        process.start()

    time.sleep(3)
    cancellation_token.set()

    for process in processes:
        process.join()

if __name__ == "__main__":
    run_examples(
        # multiprocessing_without_waiting_for_the_result,
        # multiprocessing_waiting_for_the_result,
        # multiprocessing_waiting_for_the_result_when_an_error_occurs,
        multiprocessing_with_cancellation
    )