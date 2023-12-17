import os
from openai import OpenAI
import ast
import subprocess
import sys
import random
from prompt_manager import PromptManager
from fitness_evaluator import FitnessEvaluator, GeneticAlgorithmConfig

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
            response_format={"type": "json_object"},
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

def tournament_selection(parents, tournament_size=3):
    selected_parents = []
    for _ in range(len(parents) - 2):
        tournament = random.sample(parents, tournament_size)
        winner = max(tournament, key=lambda x: x['fitness_score'])
        selected_parents.append(winner)
    return selected_parents

def apply_elitism(parents, number_of_elites=2):
    elites = sorted(parents, key=lambda x: x['fitness_score'], reverse=True)[:number_of_elites]
    return elites


def main():
    OPENAI_API_KEY = "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"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    client = initialize_openai_client()
    prompt_manager = PromptManager()
    fitness_evaluator = FitnessEvaluator()
    ga_config = GeneticAlgorithmConfig()

    initial_prompt = prompt_manager.get_number_prompt()
    response_0 = query_openai_api(client, initial_prompt)
    response_data_0 = ast.literal_eval(response_0)
    numberList = response_data_0['numberList']
    bucketSize = response_data_0['bucketSize']
    print(numberList)
    print(bucketSize)

    master_prompt = prompt_manager.get_master_prompt(numberList, bucketSize)
    response_1 = query_openai_api(client, master_prompt)
    response_data_1 = ast.literal_eval(response_1)
    master_program_code = response_data_1['program_code']
    print(master_program_code)

    if response_data_1['pip_command'] and response_data_1['pip_command'] != "None":
        install_packages(response_data_1['pip_command'])

    master_results = fitness_evaluator.evaluate_algorithm(master_program_code, numberList, bucketSize, weights={'time': 0.3, 'memory': 0.2, 'score': 0.5})
    ga_config.add_result(master_results)

    parents = []
    for individual in range(ga_config.population_size):
        valid_algorithm = False
        retries = 0
        max_retries = 3
        last_program_code = None

        while not valid_algorithm and retries < max_retries:
            try:
                parent_prompt = prompt_manager.get_parent_prompt(
                    master_program_code, response_data_1['equation'],
                    response_data_1['pseudocode'], master_results['buckets'],
                    master_results['fitness_score'], numberList, bucketSize
                )
                if retries > 0:
                    error_prompt = prompt_manager.get_repeat_prompt(last_error_message, last_program_code)
                    full_prompt = error_prompt + parent_prompt
                else:
                    full_prompt = parent_prompt
                response = query_openai_api(client, full_prompt)
                response_data = ast.literal_eval(response)
                parent_program_code = response_data.get('program_code')
                last_program_code = parent_program_code 
                print(parent_program_code)

                if not parent_program_code:
                    raise ValueError("No program code generated.")

                if response_data.get('pip_command') and response_data['pip_command'] != "None":
                    install_packages(response_data['pip_command'])

                parent_results = fitness_evaluator.evaluate_algorithm(
                    parent_program_code, numberList, bucketSize, weights={'time': 0.3, 'memory': 0.2, 'score': 0.5}
                )

                if parent_results is None or not parent_results.get('buckets'):
                    raise ValueError("Failed to evaluate algorithm or no buckets generated.")

                unique = ga_config.is_iteration_unique(parent_results)
                valid_algorithm = unique and parent_results is not None

            except ValueError as ve:
                print(f"Validation error during parent generation: {ve}. Retrying...")
                retries += 1
                valid_algorithm = False

            except Exception as e:
                last_error_message = str(e)
                print(f"An error occurred during parent generation: {e}. Retrying...")
                retries += 1
                valid_algorithm = False

        if valid_algorithm:
            ga_config.add_result(parent_results)
            parents.append(parent_results)
            print(f"Parent {individual + 1}: {parent_results}")
        else:
            print(f"Failed to generate a valid parent after {max_retries} attempts for individual {individual + 1}.")

    elite_parents = apply_elitism(parents, number_of_elites=2)
    tournament_parents = tournament_selection(parents, tournament_size=3)

    print(elite_parents)
    print(tournament_parents)
    
    children = []
    for i in range(2):
        parent1 = elite_parents[i]
        parent2 = tournament_parents[i]

        crossover_prompt = prompt_manager.get_crossover_prompt(
            parent1['program_code'], parent1['equation'], parent1['pseudocode'], parent1['buckets'], parent1['fitness_score'],
            parent2['program_code'], parent2['equation'], parent2['pseudocode'], parent2['buckets'], parent2['fitness_score'],
            numberList, bucketSize
        )
        response = query_openai_api(client, crossover_prompt)
        response_data = ast.literal_eval(response)
        child_program_code = response_data.get('program_code')
        print(child_program_code)
        if child_program_code:
            if response_data.get('pip_command') and response_data['pip_command'] != "None":
                install_packages(response_data['pip_command'])

            child_results = fitness_evaluator.evaluate_algorithm(
                child_program_code, numberList, bucketSize, weights={'time': 0.3, 'memory': 0.2, 'score': 0.5}
            )

            if child_results:
                children.append(child_results)
                print(f"Child {i + 1} generated successfully.")
            else:
                print(f"Failed to evaluate Child {i + 1}.")
        else:
            print(f"Failed to generate Child {i + 1} program code.")

    top_children = sorted(children, key=lambda x: x['fitness_score'], reverse=True)[:2]
    print("Top Children Selected for Next Generation:", top_children)

if __name__ == "__main__":
    main()