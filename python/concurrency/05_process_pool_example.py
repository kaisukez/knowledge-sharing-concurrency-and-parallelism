from concurrent.futures import ProcessPoolExecutor
from utils import timer, cpu_bound_task

@timer
def process_pool():
    print("\n=== ProcessPoolExecutor Example ===")
    numbers = [10**6, 10**6, 10**6, 10**6, 10**6]
    
    with ProcessPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(cpu_bound_task, numbers))
        print(f"Results: {results}")

if __name__ == "__main__":
    process_pool() 