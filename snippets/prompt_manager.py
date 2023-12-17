class PromptManager:
    def __init__(self):

        self.number_prompt = "..."
        self.master_prompt = "..."
        self.parent_prompt = "..."
        self.crossover_prompt = "..."
        self.mutation_prompt = "..."
        self.repeat_prompt = "..."

    def get_number_prompt(self):

        prompt = """
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

        return prompt
    
    def get_master_prompt(self, numberList, bucketSize):
        
        prompt = f"""
        Objective: Optimize and research innovative methods to enhance an algorithm's performance. Develop new mathematical approaches for superior efficiency.

        Inputs:
        - numbers: {numberList}
        - bucket_limit: {bucketSize}

        Instructions:
        1. Develop a Python function named 'optimized_bucket_filler'. This function should take two parameters: a list of numbers ('numbers') and a bucket size limit ('bucket_limit'). 
        2. The function's task is to optimize and arrange the numbers into buckets, each adhering to the bucket size limit. Each bucket should contain numbers that sum up to less than or equal to the 'bucket_limit'.
        3. Ensure that the function handles edge cases and operates safely with list manipulations to avoid errors like 'IndexError'.
        4. Create pseudocode for the 'optimized_bucket_filler' function. The pseudocode should clearly describe the logic and steps involved in the function, including handling of edge cases.
        5. The final output should consist solely of the function definition and the corresponding pseudocode. Do not include function calls or print statements in the output.
        6. If no specific pip dependencies are required for the function, default the 'pip_command' to 'None'.
        7. If external libraries are necessary (such as numpy, scipy, or scikit-learn), clearly list these dependencies in the 'pip_command' section of the JSON output and import them before the function.
        8. Ensure adherence to the following output format, formatted as JSON:
        {{
            "pip_command": "List of pip dependencies (comma-separated) or 'None' if no dependencies are required",
            "program_code": "Python function 'optimized_bucket_filler' definition",
            "pseudocode": "Pseudocode describing the logic of 'optimized_bucket_filler'",
            "equation": "Mathematical Logic in LaTeX representing the Program logic"
        }}
        """
        return prompt


    def get_parent_prompt(self, program_code_1, equation_1, pseudocode_1, buckets_1, fitness_1, numberList, bucketSize):

        prompt = """
        Objective: Further optimize and enhance an existing algorithm based on inputs from a previous iteration. Develop and refine mathematical approaches for increased efficiency, striking a balance between experimentation and exploitation.

        Parent Inputs:
        - Previous Program: 
        {}

        - Previous Mathematical Equation: 
        {}

        - Previous Pseudocode: 
        {}

        - Previous Buckets: 
        {}

        - Previous Fitness Score: 
        {}

        New Inputs:
        - numbers: {}
        - bucket_limit: {}

        Instructions:
        1. Analyze the inputs from the 'Parent' section, which includes the program, mathematical equation, pseudocode, buckets, and fitness score from the previous iteration.
        2. Develop a new or significantly refined Python function named 'optimized_bucket_filler', ensuring it does not replicate the previous program but builds upon and optimizes it.
        3. Innovate in the algorithm's approach, introducing new concepts or methods that strike a balance between leveraging the existing solution ('exploitation') and exploring new possibilities ('experimentation').
        4. Create or update pseudocode for the new 'optimized_bucket_filler' function. The pseudocode should clearly outline the innovative logic and steps, demonstrating the advancements made over the previous iteration.
        5. The function should optimize the number distribution into buckets, adhering to the 'bucket_limit', with a focus on improving the previous fitness score through innovative methods.
        6. The final output should include the new function definition, its corresponding pseudocode, and any other enhancements made over the previous iteration.
        7. If no new pip dependencies are identified, default the 'pip_command' to 'None'.
        8. If external libraries are necessary (such as numpy, scipy, or scikit-learn), clearly list these dependencies in the 'pip_command' section of the JSON output and import them before the function.
        9. Ensure adherence to the following output format, formatted as JSON:
        {{
            "pip_command": "List of pip dependencies (comma-separated) or 'None' if no dependencies are required",
            "program_code": "Python function 'optimized_bucket_filler' definition showcasing innovation and improvement",
            "pseudocode": "Updated Pseudocode for the innovative 'optimized_bucket_filler'",
            "equation": "Refined Mathematical Logic in LaTeX representing the enhanced Program logic"
        }}
        """.format(program_code_1, equation_1, pseudocode_1, buckets_1, fitness_1, numberList, bucketSize)

        return prompt
    
    def get_crossover_prompt(self, program_code_1, equation_1, pseudocode_1, buckets_1, fitness_1, 
                      program_code_2, equation_2, pseudocode_2, buckets_2, fitness_2, 
                      numberList, bucketSize):

        prompt = """
        Objective: Employ a genetic algorithm approach to combine features from two parent algorithms, creating an enhanced child algorithm that exhibits improved efficiency and innovation.

        Parent 1 Inputs:
        - Program: 
        {}

        - Mathematical Equation: 
        {}

        - Pseudocode: 
        {}

        - Buckets: 
        {}

        - Fitness Score: 
        {}

        Parent 2 Inputs:
        - Program: 
        {}

        - Mathematical Equation: 
        {}

        - Pseudocode: 
        {}

        - Buckets: 
        {}

        - Fitness Score: 
        {}

        New Inputs:
        - numbers: {}
        - bucket_limit: {}

        Instructions:
        1. Develop a new or significantly refined Python function named 'optimized_bucket_filler', building upon and optimizing the previous program.
        2. Ensure the new function innovatively approaches the algorithm's task and safely handles list manipulations to avoid errors like 'IndexError'.
        3. Create or update pseudocode for the new 'optimized_bucket_filler' function, including handling of edge cases.
        4. The function should improve the number distribution into buckets, focusing on improving the previous fitness score.
        5. The final output should include the new function definition, its corresponding pseudocode, and any enhancements made over the previous iteration.
        6. Default the 'pip_command' to 'None' if no new dependencies are identified.
        7. If external libraries are necessary (such as numpy, scipy, or scikit-learn), clearly list these dependencies in the 'pip_command' section of the JSON output and import them before the function.
        8. Ensure adherence to the following output format, formatted as JSON:
           {{
               "pip_command": "List of pip dependencies (comma-separated) or 'None' if no dependencies are required",
               "program_code": "Python function 'optimized_bucket_filler' definition showcasing innovation and improvement",
               "pseudocode": "Updated Pseudocode for the innovative 'optimized_bucket_filler'",
               "equation": "Refined Mathematical Logic in LaTeX representing the enhanced Program logic"
           }}
        """

        return prompt.format(program_code_1, equation_1, pseudocode_1, buckets_1, fitness_1, 
                      program_code_2, equation_2, pseudocode_2, buckets_2, fitness_2, 
                      numberList, bucketSize)
    
    def get_mutation_prompt(self, child_program_code, child_equation, child_pseudocode, child_buckets, child_fitness_score, numberList, bucketSize):
    
        prompt = """
        Objective: Apply the concept of mutation as part of the genetic algorithm process to the child program derived from the crossover of two parent programs. This mutation is optional and may introduce modifications for potential improvements or retain the original child program.

        Child Program Inputs:
        - Program: 
        {}

        - Mathematical Equation: 
        {}

        - Pseudocode: 
        {}

        - Buckets: 
        {}

        - Fitness Score: 
        {}

        New Inputs:
        - numbers: {}
        - bucket_limit: {}

        Instructions:
        1. Assess the child program, which is the result of combining features from two parent programs.
        2. Decide on applying mutation:
        - Option A: Retain the child program as-is if it already demonstrates optimal performance.
        - Option B: Introduce a mutation in the child program, aiming for modifications that could enhance performance.
        3. If mutation is applied, specify the changes and explain how they may improve the program.
        4. Ensure the final child program, whether mutated or not, is functional and effective.
        5. Document the decision made regarding mutation and any modifications applied.
        6. If no new pip dependencies are identified, default the 'pip_command' to 'None'.
        7. If external libraries are necessary (such as numpy, scipy, or scikit-learn), clearly list these dependencies in the 'pip_command' section of the JSON output and import them before the function.

        Output Format:
        {{
            "pip_command": "List of pip dependencies (comma-separated) or 'None' if no dependencies are required",
            "program_code": "Python function 'optimized_bucket_filler' post-mutation",
            "pseudocode": "Pseudocode of the mutated 'optimized_bucket_filler'",
            "equation": "Mathematical Logic in LaTeX representing the mutated Program logic"
        }}

        Ensure that the final output, including any mutations made, is provided in a structured JSON format as specified above. The JSON should include the pip_command, the mutated program_code, the corresponding pseudocode, and the updated equation. This format will facilitate clear interpretation and integration of the modified algorithm.
        """
        return prompt.format(child_program_code, child_equation, child_pseudocode, child_buckets, child_fitness_score, numberList, bucketSize)


    def get_repeat_prompt(self):

        prompt = """
        Contextual Note: In the process of optimizing the algorithm, it's crucial to avoid replicating any previously generated algorithms that are already recorded as parents in the GeneticAlgorithmConfig. Each iteration must be unique in terms of its approach, methodology, and results.

            Additional Instructions:
            1. When developing the new 'optimized_bucket_filler' function, ensure that the algorithm is distinct from any of the previous iterations stored in the GeneticAlgorithmConfig. This involves not only a different score and fitness score but also a unique approach to bucket distribution.
            2. Emphasize experimental and innovative mathematical methods. Consider unexplored techniques or novel applications of existing methods that can yield a distinct result.
            3. After developing the new algorithm, cross-check against the 'previous_results' stored in the GeneticAlgorithmConfig to ensure it's a unique contribution.
            4. If an iteration results in an algorithm that is not unique, take a step back, analyze why it mirrors a previous iteration, and revise the approach to ensure novelty and innovation.
            5. The ultimate goal is to push the boundaries of current methodologies, ensuring each new iteration contributes something fresh and valuable to the overall genetic algorithm optimization process.
        """

        return prompt