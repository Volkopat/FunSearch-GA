import os
from openai import OpenAI
import ast
import subprocess
import sys
import time
import psutil

def initialize_openai_client():

    try:
        client = OpenAI()
        return client
    except Exception as e:
        raise Exception(f"Failed to initialize OpenAI client: {e}")

def query_openai_api(client, prompt):

    try:
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as general_error:
        print(f"General error querying OpenAI API: {general_error}")

def install_packages(pip_command):

    if not pip_command or pip_command == "None":
        return True

    packages = pip_command.split(',')
    for package in packages:
        package = package.strip()
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing package '{package}': {e}")
            return False
    return True

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
        numberList_copy = numberList[:]
        return evaluate_algorithm(optimized_bucket_filler, numberList_copy, bucketSize, weights)
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

class GeneticAlgorithmConfig:
    def __init__(self, generations=5, population_size=6):
        self.generations = generations
        self.population_size = population_size
        self.previous_results = []  # Initialize previous results as an attribute

    def is_iteration_unique(self, current_results):
        for prev_results in self.previous_results:
            if (current_results['score'] == prev_results['score'] and
                current_results['fitness_score'] == prev_results['fitness_score'] and
                current_results['buckets'] == prev_results['buckets']):
                return False
        return True

if __name__ == "__main__":
    OPENAI_API_KEY = "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"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    client = initialize_openai_client()

    prompt_0 = """
    Objective: Generate a list of numbers and define an appropriate bucket size. The output should be structured in JSON format.

    Task Details:

    Generate Numbers:
    Create a list of random 1,2 or 3 digit numbers of any length of the list, atleast 30.
    Define Bucket Size:
    Determine a large bucket size, preferably 4 digits for the generated list of numbers.
    JSON Output Format:
    Format the output as follows:
    json
    Copy code
    {
    "numberList": [Generated list of numbers as a list],
    "bucketSize": [Defined bucket size as Integer]
    }
    Guidelines:

    Ensure the numbers and bucket size are logically consistent and applicable.
    """

    response_0 = query_openai_api(client, prompt_0)
    response_data = ast.literal_eval(response_0)
    numberList = response_data['numberList']
    bucketSize = response_data['bucketSize']
    print(numberList, '\n', bucketSize)

    prompt_1 = f"""
    Objective: Optimize and research innovative methods to enhance an algorithm's performance. Develop new mathematical approaches for superior efficiency.

    Inputs:
    - numbers: {numberList}
    - bucket_limit: {bucketSize}

    Instructions:
    1. Develop a Python function named 'optimized_bucket_filler'. This function should take two parameters: a list of numbers ('numbers') and a bucket size limit ('bucket_limit'). 
    2. The function's task is to optimize and arrange the numbers into buckets, each adhering to the bucket size limit. Each bucket should contain numbers that sum up to less than or equal to the 'bucket_limit'.
    3. Create pseudocode for the 'optimized_bucket_filler' function. The pseudocode should clearly describe the logic and steps involved in the function, providing a high-level understanding of the algorithm.
    4. The Python function should only define the logic and return a single variable 'buckets', which is a list of lists representing the optimized distribution of numbers.
    5. Do not include function calls or print statements in the output. The final output should consist solely of the function definition and the corresponding pseudocode.
    6. If no specific pip dependencies are required for the function, default the 'pip_command' to 'None'.
    7. Ensure adherence to the following output format, formatted as JSON:
    {{
        "pip_command": "List of pip dependencies (comma-separated) or 'None' if no dependencies are required",
        "program_code": "Python function 'optimized_bucket_filler' definition",
        "pseudocode": "Pseudocode describing the logic of 'optimized_bucket_filler'",
        "equation": "Mathematical Logic in LaTeX representing the Program logic"
    }}
    """
    response_1 = query_openai_api(client, prompt_1)
    response_data_1 = ast.literal_eval(response_1)
    pip_command_1 = response_data_1['pip_command']
    program_code_1 = response_data_1['program_code']
    pseudocode_1 = response_data_1['pseudocode']
    equation_1 = response_data_1['equation']
    print(program_code_1)
    print(pseudocode_1)

    ga_config = GeneticAlgorithmConfig(generations=5, population_size=6)
    print(f"Generations: {ga_config.generations}, Population Size: {ga_config.population_size}")

    if pip_command_1 and pip_command_1 != "None":
        if not install_packages(pip_command_1):
            print("Package installation failed. Proceeding with program execution.")

    weights = {'time': 0.3, 'memory': 0.2, 'score': 0.5}
    results_1 = execute_and_evaluate(program_code_1, numberList, bucketSize, weights)
    fitness_1 = results_1.get('fitness_score', 'No score calculated')
    buckets_1 = results_1.get('fitness_score', 'No score calculated')
    print(f"Results 1: {results_1}")

    prompt_2 = f"""
    Objective: Further optimize and enhance an existing algorithm based on inputs from a previous iteration. Develop and refine mathematical approaches for increased efficiency, striking a balance between experimentation and exploitation.

    Parent Inputs:
    - Previous Program: 
    {program_code_1}

    - Previous Mathematical Equation: 
    {equation_1}

    - Previous Pseudocode: 
    {pseudocode_1}

    - Previous Buckets: 
    {buckets_1}

    - Previous Fitness Score: 
    {fitness_1}

    New Inputs:
    - numbers: {numberList}
    - bucket_limit: {bucketSize}

    Instructions:
    1. Analyze the inputs from the 'Parent' section, which includes the program, mathematical equation, pseudocode, buckets, and fitness score from the previous iteration.
    2. Develop a new or significantly refined Python function named 'optimized_bucket_filler', ensuring it does not replicate the previous program but builds upon and optimizes it.
    3. Innovate in the algorithm's approach, introducing new concepts or methods that strike a balance between leveraging the existing solution ('exploitation') and exploring new possibilities ('experimentation').
    4. Create or update pseudocode for the new 'optimized_bucket_filler' function. The pseudocode should clearly outline the innovative logic and steps, demonstrating the advancements made over the previous iteration.
    5. The function should optimize the number distribution into buckets, adhering to the 'bucket_limit', with a focus on improving the previous fitness score through innovative methods.
    6. The final output should include the new function definition, its corresponding pseudocode, and any other enhancements made over the previous iteration.
    7. If no new pip dependencies are identified, default the 'pip_command' to 'None'.
    8. Ensure adherence to the following output format, formatted as JSON:
    {{
        "pip_command": "List of pip dependencies (comma-separated) or 'None' if no dependencies are required",
        "program_code": "Python function 'optimized_bucket_filler' definition showcasing innovation and improvement",
        "pseudocode": "Updated Pseudocode for the innovative 'optimized_bucket_filler'",
        "equation": "Refined Mathematical Logic in LaTeX representing the enhanced Program logic"
    }}
    """
    additional_prompt = """
    Contextual Note: In the process of optimizing the algorithm, it's crucial to avoid replicating any previously generated algorithms that are already recorded as parents in the GeneticAlgorithmConfig. Each iteration must be unique in terms of its approach, methodology, and results.

    Additional Instructions:
    1. When developing the new 'optimized_bucket_filler' function, ensure that the algorithm is distinct from any of the previous iterations stored in the GeneticAlgorithmConfig. This involves not only a different score and fitness score but also a unique approach to bucket distribution.
    2. Emphasize experimental and innovative mathematical methods. Consider unexplored techniques or novel applications of existing methods that can yield a distinct result.
    3. After developing the new algorithm, cross-check against the 'previous_results' stored in the GeneticAlgorithmConfig to ensure it's a unique contribution.
    4. If an iteration results in an algorithm that is not unique, take a step back, analyze why it mirrors a previous iteration, and revise the approach to ensure novelty and innovation.
    5. The ultimate goal is to push the boundaries of current methodologies, ensuring each new iteration contributes something fresh and valuable to the overall genetic algorithm optimization process.
    """

    response_2 = query_openai_api(client, prompt_2)
    response_data_2 = ast.literal_eval(response_2)
    pip_command_2 = response_data_2['pip_command']
    program_code_2 = response_data_2['program_code']
    pseudocode_2 = response_data_2['pseudocode']
    equation_2 = response_data_2['equation']
    print(program_code_2)
    print(pseudocode_2)

    if pip_command_2 and pip_command_2 != "None":
        if not install_packages(pip_command_2):
            print("Package installation failed. Proceeding with program execution.")

    weights = {'time': 0.3, 'memory': 0.2, 'score': 0.5}
    results_2 = execute_and_evaluate(program_code_2, numberList, bucketSize, weights)
    fitness_2 = results_2.get('fitness_score', 'No score calculated')
    buckets_2 = results_2.get('buckets', 'No score calculated')
    print(f"Results 2: {results_2}")

    ga_config = GeneticAlgorithmConfig()
    weights = {'time': 0.3, 'memory': 0.2, 'score': 0.5}
    for i in range(ga_config.population_size):
        results = execute_and_evaluate(program_code_2, numberList, bucketSize, weights)
        if not ga_config.is_iteration_unique(results):
            print("Generated iteration is not unique, retrying...")
            continue  

        ga_config.previous_results.append(results)
        print(f"Results {i+1}: {results}")