import time
import os, sys
import shutil
from statistics import mean
import importlib
import numpy as np

def delete_pycache():
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')

def benchmark_module_import():
    start_time = time.perf_counter()
    if 'module' in sys.modules:
        importlib.reload(sys.modules['module'])
    else:
        import module
    end_time = time.perf_counter()
    return end_time - start_time

def benchmark_module_import_times(n):
    delete_pycache()  # Ensure pycache is deleted at the start
    times_without_cache = benchmark_module_import()  # Benchmark without cache
    times_with_cache = benchmark_module_import()  # Benchmark with cache (pycache now exists)
    return times_without_cache, times_with_cache

def benchmark(num):
    n_values = list(range(10, 101, 10))  # Or adjust as needed
    avg_of_avg_times_without_cache = []
    avg_of_avg_times_with_cache = []
    for i in range(num):
        avg_times_without_cache = []
        avg_times_with_cache = []
        for n in n_values:
            without_cache, with_cache = benchmark_module_import_times(n)
            avg_times_without_cache.append(without_cache)
            avg_times_with_cache.append(with_cache)
        avg_of_avg_times_without_cache.append(avg_times_without_cache)
        avg_of_avg_times_with_cache.append(avg_times_with_cache)
    without_cache_arr = np.array(avg_of_avg_times_without_cache)
    with_cache_arr = np.array(avg_of_avg_times_with_cache)
    without_average = np.mean(without_cache_arr, axis=0)
    with_average = np.mean(with_cache_arr, axis=0)
    return n_values, without_average.tolist(), with_average.tolist()