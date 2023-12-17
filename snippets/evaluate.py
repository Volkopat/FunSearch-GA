numberList_1 = [12, 34, 56, 78, 90, 23, 45, 67, 89, 10] 
bucketSize_1 = 100
program_code_1 = """
def optimized_bucket_filler(numbers, bucket_limit):
    numbers.sort(reverse=True)
    buckets = []
    while numbers:
        bucket = []
        total = 0
        idx = 0
        while idx < len(numbers):
            if total + numbers[idx] <= bucket_limit:
                total += numbers[idx]
                bucket.append(numbers.pop(idx))
            else:
                idx += 1
        buckets.append(bucket)
    return buckets
"""

numberList_2 = [12, 57, 89, 24, 46, 35, 67, 78, 50] 
bucketSize_2 = 100
program_code_2 = """
def optimized_bucket_filler(numbers, bucket_limit):
    buckets = []
    for number in sorted(numbers, reverse=True):
        placed = False
        for bucket in buckets:
            if sum(bucket) + number <= bucket_limit:
                bucket.append(number)
                placed = True
                break
        if not placed:
            buckets.append([number])
    return buckets
"""

numberList_3 = [14, 85, 29, 52, 67, 33, 90, 24, 76, 58] 
bucketSize_3 = 100
program_code_3 = """
def optimized_bucket_filler(numbers, bucket_limit):
    numbers.sort(reverse=True)
    buckets = []

    for number in numbers:
        placed = False
        for bucket in buckets:
            if sum(bucket) + number <= bucket_limit:
                bucket.append(number)
                placed = True
                break
        if not placed:
            buckets.append([number])

    return buckets
"""
def execute_program(program_code):
    try:
        local_scope = {}
        exec(program_code, globals(), local_scope)
        return local_scope.get('optimized_bucket_filler')
    except Exception as e:
        print(f"Error executing program: {e}")
        return None
    
# buckets_1 = execute_program(program_code_1, numberList_1, bucketSize_1)
# print(buckets_1)
# buckets_2 = execute_program(program_code_2, numberList_2, bucketSize_2)
# print(buckets_2)
# buckets_3 = execute_program(program_code_3, numberList_3, bucketSize_3)
# print(buckets_3)

import time
import psutil
import os

def execute_program(program_code):
    try:
        local_scope = {}
        exec(program_code, globals(), local_scope)
        return local_scope.get('optimized_bucket_filler')
    except Exception as e:
        print(f"Error executing program: {e}")
        return None

def measure_time(func, *args, **kwargs):

    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result

def measure_memory(func, *args, **kwargs):

    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    result = func(*args, **kwargs)
    memory_after = process.memory_info().rss
    return memory_after - memory_before, result

def scoring_function(buckets, bucket_limit):

    total_empty_space = sum(bucket_limit - sum(bucket) for bucket in buckets)
    score = (1000 - total_empty_space) - (10 * len(buckets))
    
    return score

def execute_and_evaluate(program_code, numberList, bucketSize, weights):
    optimized_bucket_filler = execute_program(program_code)
    if callable(optimized_bucket_filler):
        return evaluate_algorithm(optimized_bucket_filler, numberList, bucketSize, weights)
    else:
        print("Function 'optimized_bucket_filler' not found in the provided code.")
        return None

def calculate_fitness_score(time_taken, memory_used, custom_score, weights):

    normalized_time_score = 100 / (1 + time_taken)
    normalized_memory_score = 100 / (1 + memory_used)
    normalized_custom_score = (custom_score / 1000) * 100

    fitness_score = (weights['time'] * normalized_time_score +
                     weights['memory'] * normalized_memory_score +
                     weights['score'] * normalized_custom_score)
    return fitness_score

def evaluate_algorithm(algorithm_func, numberList, bucket_limit, weights):

    time_taken, buckets = measure_time(algorithm_func, numberList, bucket_limit)
    memory_used, _ = measure_memory(algorithm_func, numberList, bucket_limit)
    score = scoring_function(buckets, bucket_limit)
    fitness_score = calculate_fitness_score(time_taken, memory_used, score, weights)

    return {
        "time_taken": time_taken,
        "memory_used": memory_used,
        "score": score,
        "fitness_score": fitness_score,
        "buckets": buckets
    }

if __name__ == "__main__":
    weights = {'time': 0.3, 'memory': 0.2, 'score': 0.5}
    results_1 = execute_and_evaluate(program_code_1, numberList_1, bucketSize_1, weights)
    fitness_1 = results_1.get('fitness_score', 'No score calculated')
    results_2 = execute_and_evaluate(program_code_2, numberList_2, bucketSize_2, weights)
    fitness_2 = results_2.get('fitness_score', 'No score calculated')
    results_3 = execute_and_evaluate(program_code_3, numberList_3, bucketSize_3, weights)
    fitness_3 = results_3.get('fitness_score', 'No score calculated')

    print(f"Results 1: {results_1}, Fitness Score: {fitness_1}")
    print(f"Results 2: {results_2}, Fitness Score: {fitness_2}")
    print(f"Results 3: {results_3}, Fitness Score: {fitness_3}")