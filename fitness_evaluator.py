import os
import re
import time
import psutil

class FitnessEvaluator:
    @staticmethod
    def execute_program(program_code):
        try:
            local_scope = {}
            exec(program_code, globals(), local_scope)
            return local_scope.get('optimized_bucket_filler')
        except NameError as e:
            match = re.search(r"name '(\w+)' is not defined", str(e))
            if match:
                missing_module = match.group(1)
                full_code = f"import {missing_module}\n" + program_code
                try:
                    exec(full_code, globals(), local_scope)
                    return local_scope.get('optimized_bucket_filler')
                except Exception as e_inner:
                    print(f"Error executing program after adding import: {e_inner}")
            else:
                print(f"Error executing program: {e}")
        except Exception as e:
            print(f"Error executing program: {e}")

        return None

    @staticmethod
    def measure_time(func, *args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time, result

    @staticmethod
    def measure_memory(func, *args, **kwargs):
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        result = func(*args, **kwargs)
        memory_after = process.memory_info().rss
        return memory_after - memory_before, result

    @staticmethod
    def scoring_function(buckets, bucket_limit):
        total_empty_space = sum(bucket_limit - sum(bucket) for bucket in buckets)
        distribution_score = FitnessEvaluator.calculate_distribution_score(buckets)
        variance_score = FitnessEvaluator.calculate_variance_score(buckets, bucket_limit)
        score = (1000 - total_empty_space) - (10 * len(buckets)) + distribution_score + variance_score

        return max(score, 0)  # Ensure the score is not negative

    @staticmethod
    def calculate_distribution_score(buckets):
        if not buckets:
            return 0
        average_fill = sum(sum(bucket) for bucket in buckets) / len(buckets)
        return 100 - sum(abs(sum(bucket) - average_fill) for bucket in buckets) / len(buckets)

    @staticmethod
    def calculate_variance_score(buckets, bucket_limit):
        if not buckets:
            return 0
        total_variance = sum((sum(bucket) - bucket_limit / 2) ** 2 for bucket in buckets) / len(buckets)
        return 100 - total_variance / (bucket_limit / 2) ** 2

    @staticmethod
    def calculate_fitness_score(time_taken, memory_used, custom_score, weights):
        normalized_time_score = 100 / (1 + time_taken)
        normalized_memory_score = 100 / (1 + memory_used)
        normalized_custom_score = (custom_score / 1000) * 100
        fitness_score = (weights['time'] * normalized_time_score +
                         weights['memory'] * normalized_memory_score +
                         weights['score'] * normalized_custom_score)
        return fitness_score

    @staticmethod
    def evaluate_algorithm(program_code_str, numberList, bucket_limit, weights):
        algorithm_func = FitnessEvaluator.execute_program(program_code_str)

        if callable(algorithm_func):
            numberList_copy = numberList[:]
            time_taken, buckets = FitnessEvaluator.measure_time(algorithm_func, numberList_copy, bucket_limit)
            memory_used, _ = FitnessEvaluator.measure_memory(algorithm_func, numberList_copy, bucket_limit)
            score = FitnessEvaluator.scoring_function(buckets, bucket_limit)
            fitness_score = FitnessEvaluator.calculate_fitness_score(time_taken, memory_used, score, weights)

            return {
                "time_taken": time_taken,
                "memory_used": memory_used,
                "score": score,
                "fitness_score": fitness_score,
                "buckets": buckets
            }
        else:
            print("Function 'optimized_bucket_filler' not found in the provided code.")
            return None

class GeneticAlgorithmConfig:
    def __init__(self, generations=5, population_size=6):
        self.generations = generations
        self.population_size = population_size
        self.previous_results = []

    def is_iteration_unique(self, current_results):
        for prev_results in self.previous_results:
            if (current_results['score'] == prev_results['score'] and
                current_results['fitness_score'] == prev_results['fitness_score']):
                return False
        return True

    def add_result(self, result):
        self.previous_results.append(result)
