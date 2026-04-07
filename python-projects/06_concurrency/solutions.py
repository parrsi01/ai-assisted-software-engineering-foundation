"""
Module 06: Concurrency — Solutions
threading, multiprocessing, asyncio
"""
import threading
import multiprocessing
import asyncio
import time
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# --- Threading ---

class SafeCounter:
    """Thread-safe counter using a Lock."""
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:  # only one thread can execute this block at a time
            self._count += 1

    def value(self) -> int:
        with self._lock:
            return self._count


def threaded_sum(numbers: list[int], num_threads: int = 4) -> int:
    """Sum a large list using multiple threads (I/O-bound demo).
    Note: for CPU-bound work, use multiprocessing due to the GIL.
    """
    chunk_size = len(numbers) // num_threads
    results = [0] * num_threads
    threads = []

    def sum_chunk(idx: int, chunk: list[int]):
        results[idx] = sum(chunk)

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(numbers)
        t = threading.Thread(target=sum_chunk, args=(i, numbers[start:end]))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # wait for all threads to finish

    return sum(results)


# --- Producer-Consumer with Queue ---

def producer_consumer_demo(items: list, process_fn=None) -> list:
    """Classic producer-consumer pattern using queue.Queue."""
    if process_fn is None:
        process_fn = lambda x: x * 2

    task_queue = queue.Queue()
    results = []
    results_lock = threading.Lock()

    def producer():
        for item in items:
            task_queue.put(item)
        task_queue.put(None)  # sentinel to signal done

    def consumer():
        while True:
            item = task_queue.get()
            if item is None:
                task_queue.put(None)  # pass sentinel to next consumer (if any)
                break
            result = process_fn(item)
            with results_lock:
                results.append(result)
            task_queue.task_done()

    prod = threading.Thread(target=producer)
    cons = threading.Thread(target=consumer)
    prod.start(); cons.start()
    prod.join(); cons.join()

    return sorted(results)


# --- Multiprocessing ---

def cpu_bound_task(n: int) -> int:
    """CPU-intensive: sum of squares up to n."""
    return sum(i * i for i in range(n))


def parallel_cpu_work(tasks: list[int]) -> list[int]:
    """Run CPU-bound tasks in parallel across processes (bypasses GIL)."""
    with ProcessPoolExecutor() as executor:
        return list(executor.map(cpu_bound_task, tasks))


# --- asyncio ---

async def fetch_data(url: str, delay: float = 0.1) -> dict:
    """Simulate an async HTTP GET (using sleep as stand-in for network I/O)."""
    await asyncio.sleep(delay)  # non-blocking wait
    return {"url": url, "status": 200, "data": f"content from {url}"}


async def fetch_all(urls: list[str]) -> list[dict]:
    """Fetch all URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)  # run all tasks concurrently, wait for all


async def fetch_with_timeout(url: str, timeout: float = 1.0) -> dict | None:
    """Fetch with timeout — returns None on timeout."""
    try:
        return await asyncio.wait_for(fetch_data(url), timeout=timeout)
    except asyncio.TimeoutError:
        return None


# --- Semaphore for rate limiting ---

async def rate_limited_fetch(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    """Limit concurrent requests with a semaphore."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url):
        async with semaphore:  # blocks if max_concurrent already running
            return await fetch_data(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])


if __name__ == "__main__":
    # Thread-safe counter
    counter = SafeCounter()
    threads = [threading.Thread(target=counter.increment) for _ in range(1000)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert counter.value() == 1000

    # Threaded sum
    nums = list(range(1000))
    assert threaded_sum(nums) == sum(nums)

    # Producer-consumer
    results = producer_consumer_demo([1, 2, 3, 4, 5])
    assert results == [2, 4, 6, 8, 10]

    # asyncio
    urls = [f"https://api.example.com/{i}" for i in range(5)]
    results = asyncio.run(fetch_all(urls))
    assert len(results) == 5
    assert all(r["status"] == 200 for r in results)

    # Timeout
    result = asyncio.run(fetch_with_timeout("https://slow.example.com", timeout=0.001))
    assert result is None

    print("All assertions passed.")
