Initialize FunSearch with a pre-trained LLM and an automated evaluator:

1. Define a fitness function that evaluates how good a solution (program) is.
2. Define a seed program based on common knowledge of the problem domain.
3. Initialize a pool of programs starting with the seed program.

Begin the iterative FunSearch process:

WHILE termination conditions are not met DO
    1. Select a subset of the best-scoring programs from the current pool.
    2. Provide these programs to the LLM as a basis for generating new solutions.
    3. LLM generates new programs based on the input programs.
    4. Use the automated evaluator to execute and evaluate the new programs:
        a. Compute the fitness for each new program.
        b. Validate the correctness of each program (guard against hallucinations).
    5. Add the highest-scoring valid programs back into the pool.
    6. Optionally, introduce mutations or variations to enhance diversity.
    7. If running in parallel, synchronize the pool across different threads/processes.
    
    // This can be considered as one generation in an evolutionary algorithm.

    8. Check for termination conditions, which could be:
        a. A satisfactory fitness level has been reached for any program.
        b. A predefined number of generations has been reached.
        c. No significant improvement has been observed for a certain number of generations.

Output the best solution(s) from the pool of programs.
