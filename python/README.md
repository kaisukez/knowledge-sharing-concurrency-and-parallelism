Python

1. Threading
    - Results are not returned, need to implement custom solution (e.g., queue or shared list)
    - Errors don't propagate to the main thread
    - Can't be cancelled natively, need to implement custom solution (e.g., Event)
    - Need locking mechanism when multiple threads do non-atomic operations with shared variables
    - Limited by GIL (Global Interpreter Lock)
        - Even though threads can run on different CPU cores, but the GIL prevents multiple threads from executing Python code simultaneously

2. Thread Pool
    - Results are returned in order
    - Errors propagate to the main thread
        - But need to implement your own exception aggregation (not a big deal, it's easy to implement anyway)
    - Can't be cancelled natively, need to implement custom solution (e.g., Event)
    - Need locking mechanism when multiple threads do non-atomic operations with shared variables
    - Limited by GIL (Global Interpreter Lock)
        - Even though threads can run on different CPU cores, but the GIL prevents multiple threads from executing Python code simultaneously

3. Asyncio
    - Results are returned in order
    - Errors propagate to the main thread
        - No need to implement your own exception aggregation (built-in with return_exceptions=True)
    - Can be cancelled natively (task.cancel())
    - No need for locking mechanism (single-threaded event loop)
    - Can convert non-blocking functions that work like blocking to actual non-blocking (for legacy libraries)
        - asyncio.to_thread() for I/O-bound tasks
    - Can run any function in a separate process (using process pool), and await them!
        

4. Multiprocessing
    - Results are not returned, need to implement custom solution (e.g., Manager or shared memory)
    - Errors don't propagate to the main process
    - Can't be cancelled natively, need to implement custom solution (e.g., Event or Value)
    - Need locking mechanism when multiple processes do non-atomic operations with shared variables
    - Not limited by GIL (true parallelism)
        - Each process has its own GIL, allowing true parallel execution across CPU cores

5. Process Pool
    - Results are returned in order
    - Errors propagate to the main process
        - But need to implement your own exception aggregation (not a big deal, it's easy to implement anyway)
    - Can't be cancelled natively, need to implement custom solution (e.g., Manager.dict)
    - Need locking mechanism when multiple processes do non-atomic operations with shared variables
    - Not limited by GIL (true parallelism)
        - Each process has its own GIL, allowing true parallel execution across CPU cores