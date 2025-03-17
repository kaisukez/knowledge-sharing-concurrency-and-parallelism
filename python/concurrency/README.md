Python

1. Threading
    - Results are not returned
    - Errors don't propergate to the main thread
    - Can't be cancelled natively, need to implement custom solution

2. Thread Pool
    - Results are returned in order
    - Errors propergate to the main thread
        - But need to implement your own exception aggregation (not a big deal, it's easy to implement anyway)
    - Can't be cancelled natively, need to implement custom solution

3. Asyncio
    - Results are returned in order
    - Errors propergate to the main thread
        - No need to implement your own exception aggregation
    - Can cancelled natively, no need to implement custom solution
    - Can convert blocking-io tasks into non-blocking in case working with legacy libraries that don't support asyncio