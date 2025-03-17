import multiprocessing
from utils import timer, cpu_bound_task

@timer
def basic_multiprocessing():
    print("\n=== Basic Multiprocessing Example ===")
    processes = []
    numbers = [10**6, 10**6, 10**6, 10**6, 10**6]
    
    for i, n in enumerate(numbers):
        process = multiprocessing.Process(
            target=cpu_bound_task,
            args=(n,)
        )
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

if __name__ == "__main__":
    basic_multiprocessing() 