from concurrent.futures import ProcessPoolExecutor, as_completed

# Global worker function
def worker(args):
    i, y, z, a = args  # Unpack the arguments
    return A(i, y, z, a)

def A(x, y, z, a):
    # Example implementation of A
    return x + y + z + a  # Replace this with the actual computation

def check_parallel_cpu_bound(y, z, a, N):
    # Use ProcessPoolExecutor for parallelism
    with ProcessPoolExecutor() as executor:
        # Prepare arguments for each task
        tasks = [(i, y, z, a) for i in range(1000)]
        
        # Submit tasks to the pool
        futures = {executor.submit(worker, task): task for task in tasks}
        
        # Process results as they complete
        for future in as_completed(futures):
            result = future.result()
            if result == N:
                # Optionally shut down the pool early (if desired)
                executor.shutdown(wait=False)
                return True  # Return True if any result matches N

    return False  # Return False if no result matches N

if __name__ == '__main__':
    # Example values
    y, z, a, N = 2, 3, 4, 10  
    result_found = check_parallel_cpu_bound(y, z, a, N)
    if result_found:
        print(f"Found a result matching {N}.")
    else:
        print(f"No result matches {N}.")