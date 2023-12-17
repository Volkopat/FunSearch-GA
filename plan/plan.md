# Plan of execution: Bit Packing Algorithm:
## Initialization:
- Initialize connection with OpenAI
- Initialize number of generations - **generations**
- Initialize population size - **population_size**
- **Prompt 1** Perform first LLM Request to only provide the numbers and the bucket limit.
    - Store them as: **numbers[list]** and **bucket_limit - int**
- Store seed program in the string called **seed**.
- Store the equation of the program in **equation**.
- We run compile(seed) and exec(seed(numbers, bucket_limit)) -> **buckets**, **bucket_limit**.
- We then pass these results to scorer(buckets, bucket_limit) -> **score**.

## LLM Preparation:
- **Prompt 2** Tell LLM your goal to optimize and research novel ways to improve and optimize the algorithm, develop new mathematics for better performance.
    - Pass the **numbers**, **bucket_limit**, **seed**, **equation**, **buckets** and **score** as input
    - Instruct it to strictly produce a json with format:
    result = {
        "pip": (pip dependencies that can be installed via pip install comma separated)
        "Program": {Optimized Program},
        "Equation": {Optimized Program Equation}.
    }
- Parse the JSON data to extract the contents -> **pip_dependencies**, **optimized_program**, **optimized_equation**
- Install pip dependencies and run exec(JSON Program) -> **optimized_score**

## Genetic Algorithm:
- Initialize parents[json]:
- Run for loop on population_size:
    - Run **Prompt 2** to produce diverse results producing **pip_dependencies**, **optimized_program**, **optimized_equation**
- Run for loop on generations:
    - Initialize **fitness[list]**
    - Calculate fitness - Install pip dependencies and run exec(JSON Program) for each parent -> **fitness**
    - Initialize **new_parents[json]**
    - Run for loop on parents:
        - Select **number_of_parents** parents based on **fitness**
        - Apply Cross over to create offspring
        - Apply Mutation on offspring
        - Append to **new_parents**
    - **parents** = **new_parents**

## Select Parents:
- **Prompt 3** Tell the LLM that this is the selection of parents part of genetic algorithm where the **new_parents** and **fitness** is fed. Based on this it will decide **number_of_parents** and produce the list of parents selected along with they json data in a form of a list to be sent to cross over.

## Cross Over:
- **Prompt 4** Tell the LLM that this is the cross over part of the genetic algorithm and feed it the **number_of_parents** selected parents as a list of json to produce a json result similar to Prompt 2.
    - Pass the properties of **number_of_parents** parents.
    - Instruct it to strictly produce a json with format:
    result = {
        "pip": (pip dependencies that can be installed via pip install comma separated)
        "Program": {Cross Over Program},
        "Equation": {Cross Over Program Equation}.
    }
- Parse the JSON data to extract the contents -> **pip_dependencies**, **optimized_program**, **optimized_equation**

## Mutation:
- **Prompt 5** Tell the LLM that this is the optional mutation part of the genetic algorithm and feed it the two selected parents to produce a json result similar to Prompt 2.
    - Pass the properties of cross over program.
    - Instruct it to strictly produce a json with format:
    result = {
        "pip": (pip dependencies that can be installed via pip install comma separated)
        "Program": {Mutated Program},
        "Equation": {Mutated Program Equation}.
    }
- Parse the JSON data to extract the contents -> **pip_dependencies**, **optimized_program**, **optimized_equation**

## Output:
- Final result should be the highest score of the optimized algorithm, the python implementation, the math equation and the results.