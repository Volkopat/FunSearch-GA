import os
import ast
import subprocess
import sys
import random
import logging
from dotenv import load_dotenv
from openai import OpenAI
from prompt_manager import PromptManager
from fitness_evaluator import FitnessEvaluator, GeneticAlgorithmConfig
load_dotenv()

logging.basicConfig(filename='genetic_algorithm.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_openai_client():

    try:
        client = OpenAI()
        return client
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client: {e}")
        raise

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
        logging.error(f"General error querying OpenAI API: {general_error}")

def install_packages(pip_command):

    if not pip_command or pip_command == "None":
        return True
    packages = pip_command.split(',')
    for package in packages:
        package = package.strip()
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            logging.error(f"Error installing package '{package}': {e}")
            return False
    return True

def tournament_selection(parents, tournament_size=3):

    selected_parents = []
    for _ in range(len(parents) - 2):
        tournament = random.sample(parents, tournament_size)
        winner = max(tournament, key=lambda x: x['evaluation_results']['fitness_score'])
        selected_parents.append(winner)
    return selected_parents

def apply_elitism(parents, number_of_elites=2):

    elites = sorted(parents, key=lambda x: x['evaluation_results']['fitness_score'], reverse=True)[:number_of_elites]
    return elites

def log_program_details(program_info, title=None):

    if title:
        logging.info(f"----- {title} -----")

    if 'program_code' in program_info:
        logging.info(f"Program Code:\n{program_info['program_code']}")

    if 'equation' in program_info:
        logging.info(f"Equation:\n{program_info['equation']}")

    if 'pseudocode' in program_info:
        logging.info(f"Pseudocode:\n{program_info['pseudocode']}")

    if 'evaluation_results' in program_info:
        eval_results = program_info['evaluation_results']
        logging.info("Evaluation Results:")
        logging.info(f"Time Taken: {eval_results.get('time_taken', 'N/A')}")
        logging.info(f"Memory Used: {eval_results.get('memory_used', 'N/A')}")
        logging.info(f"Score: {eval_results.get('score', 'N/A')}")
        logging.info(f"Fitness Score: {eval_results.get('fitness_score', 'N/A')}")
        logging.info(f"Buckets: {eval_results.get('buckets', 'N/A')}")

    if 'pip_command' in program_info and program_info['pip_command'] not in ["None", None, ""]:
        install_packages(program_info['pip_command'])

def query_and_log_initial_data(prompt_manager, client, fitness_evaluator, ga_config):
    try:
        initial_prompt = prompt_manager.get_number_prompt()
        response_0 = query_openai_api(client, initial_prompt)
        response_data_0 = ast.literal_eval(response_0)
        numberList = response_data_0['numberList']
        bucketSize = response_data_0['bucketSize']
        logging.info(f"Number List: {numberList}")
        logging.info(f"Bucket Size: {bucketSize}")

        master_prompt = prompt_manager.get_master_prompt(numberList, bucketSize)
        response_1 = query_openai_api(client, master_prompt)
        response_data_1 = ast.literal_eval(response_1)
        log_program_details(response_data_1, "Master Program Details")

        if 'pip_command' in response_data_1 and response_data_1['pip_command'] not in ["None", None, ""]:
            install_packages(response_data_1['pip_command'])

        master_results = fitness_evaluator.evaluate_algorithm(response_data_1['program_code'], numberList, bucketSize, weights={'time': 0.3, 'memory': 0.2, 'score': 0.5})
        ga_config.add_result(master_results)
        log_program_details(master_results, "Master Results Evaluation")

        return {
            'numberList': numberList,
            'bucketSize': bucketSize,
            'program_code': response_data_1['program_code'],
            'equation': response_data_1.get('equation', ''),
            'pseudocode': response_data_1.get('pseudocode', ''),
            **master_results
        }

    except Exception as e:
        logging.error("An error occurred: ", exc_info=True)


def generate_parents(prompt_manager, client, fitness_evaluator, ga_config, master_program_details):

    parents = []
    for individual in range(ga_config.population_size):
        valid_algorithm = False
        retries = 0
        max_retries = 3
        last_program_code = None
        last_error_message = None

        while not valid_algorithm and retries < max_retries:
            try:
                parent_prompt = prompt_manager.get_parent_prompt(
                    master_program_details['program_code'], 
                    master_program_details['equation'], 
                    master_program_details['pseudocode'], 
                    master_program_details['buckets'], 
                    master_program_details['fitness_score'], 
                    master_program_details['numberList'], 
                    master_program_details['bucketSize']
                )
                full_prompt = prompt_manager.get_repeat_prompt(last_error_message, last_program_code) + parent_prompt if retries > 0 else parent_prompt
                response = query_openai_api(client, full_prompt)
                response_data = ast.literal_eval(response)
                parent_program_code = response_data.get('program_code')
                last_program_code = parent_program_code
                print

                if not parent_program_code:
                    raise ValueError("No program code generated.")

                if response_data.get('pip_command') and response_data['pip_command'] != "None":
                    install_packages(response_data['pip_command'])

                parent_results = fitness_evaluator.evaluate_algorithm(
                    parent_program_code, 
                    master_program_details['numberList'], 
                    master_program_details['bucketSize'], 
                    weights={'time': 0.3, 'memory': 0.2, 'score': 0.5}
                )

                if parent_results is None or not parent_results.get('buckets'):
                    raise ValueError("Failed to evaluate algorithm or no buckets generated.")

                unique = ga_config.is_iteration_unique(parent_results)
                valid_algorithm = unique and parent_results is not None

            except ValueError as ve:
                logging.warning(f"Validation error during parent generation: {ve}. Retrying...")
                retries += 1
                valid_algorithm = False

            except Exception as e:
                last_error_message = str(e)
                logging.error(f"An error occurred during parent generation: {e}. Retrying...")
                retries += 1
                valid_algorithm = False

        if valid_algorithm:
            parent_info = {
                'program_code': parent_program_code,
                'evaluation_results': parent_results,
                'equation': response_data.get('equation'),
                'pseudocode': response_data.get('pseudocode')
            }
            ga_config.add_result(parent_results)
            parents.append(parent_info)
            log_program_details(parent_info, f"Parent {individual + 1} Details")
        else:
            logging.error(f"Failed to generate a valid parent after {max_retries} attempts for individual {individual + 1}.")

    return parents

def generate_children(prompt_manager, client, fitness_evaluator, parents, numberList, bucketSize, elite_count=2, tournament_size=3):

    elite_parents = apply_elitism(parents, number_of_elites=elite_count)
    tournament_parents = tournament_selection(parents, tournament_size=tournament_size)

    children = []
    for i in range(2):
        parent1, parent2 = elite_parents[i], tournament_parents[i]
        log_program_details(parent1, f"Crossover Details for Child {i + 1} - Elite Parent Details")
        log_program_details(parent2, "Tournament Parent Details")

        crossover_prompt = prompt_manager.get_crossover_prompt(
            parent1['program_code'], parent1['equation'], parent1['pseudocode'], parent1['evaluation_results']['buckets'], parent1['evaluation_results']['fitness_score'],
            parent2['program_code'], parent2['equation'], parent2['pseudocode'], parent2['evaluation_results']['buckets'], parent2['evaluation_results']['fitness_score'],
            numberList, bucketSize
        )
        response = query_openai_api(client, crossover_prompt)
        response_data = ast.literal_eval(response)
        child_program_code = response_data.get('program_code')

        if child_program_code:
            if response_data.get('pip_command') and response_data['pip_command'] != "None":
                install_packages(response_data['pip_command'])

            child_results = fitness_evaluator.evaluate_algorithm(
                child_program_code, numberList, bucketSize, weights={'time': 0.3, 'memory': 0.2, 'score': 0.5}
            )

            if child_results:
                child_info = {
                    'program_code': child_program_code,
                    'evaluation_results': child_results,
                    'equation': response_data.get('equation'),
                    'pseudocode': response_data.get('pseudocode')
                }
                children.append(child_info)
                log_program_details(child_info, f"Child {i + 1} Details")
            else:
                logging.error(f"Failed to evaluate Child {i + 1}.")
        else:
            logging.error(f"Failed to generate Child {i + 1} program code.")

    top_children = sorted(children, key=lambda x: x['evaluation_results']['fitness_score'], reverse=True)[:2]
    logging.info(f"Top Children Selected for Next Generation: {top_children}")
    return top_children

def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    client = initialize_openai_client()
    prompt_manager = PromptManager()
    fitness_evaluator = FitnessEvaluator()
    ga_config = GeneticAlgorithmConfig()

    try:
        master_program_details = query_and_log_initial_data(prompt_manager, client, fitness_evaluator, ga_config)
        parents = generate_parents(prompt_manager, client, fitness_evaluator, ga_config, master_program_details)
        top_children = generate_children(prompt_manager, client, fitness_evaluator, parents, master_program_details['numberList'], master_program_details['bucketSize'])

        logging.info(f"Top Children Selected for Next Generation: {top_children}")

    except Exception as e:
        logging.error("An error occurred in the main process: ", exc_info=True)

if __name__ == "__main__":
    main()
