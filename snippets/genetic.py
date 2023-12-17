import random

# Define a function to visually represent the individual as a string for easier understanding
def individual_to_string(individual):
    """ Convert an individual's list of bits to a string for display. """
    return ''.join(str(bit) for bit in individual)

# Modify the functions with detailed comments explaining each step
def generate_individual(length):
    """ Generates a random individual consisting of a list of bits (0s and 1s). """
    individual = [random.randint(0, 1) for _ in range(length)]
    # Display the generated individual as a string of bits for better intuition
    print(f"Generated individual: {individual_to_string(individual)}")
    return individual

def compute_fitness(individual):
    """ Computes the fitness of an individual by summing the bits. Higher sum equals higher fitness. """
    fitness = sum(individual)  # The fitness function is the sum of all the bits
    # Display the computed fitness along with the individual represented as a string
    print(f"Computed fitness: {fitness} for individual: {individual_to_string(individual)}")
    return fitness

def select_parents(population, fitnesses):
    """ Selects two parents from the population based on their fitness. Higher fitness increases chance of selection. """
    # Randomly choose two parents with a probability weighted by their fitness
    parents = random.choices(population, weights=fitnesses, k=2)
    # Display the selected parents for crossover
    print(f"Selected parents for crossover: {individual_to_string(parents[0])} and {individual_to_string(parents[1])}")
    return parents

def crossover(parent1, parent2):
    """ Performs crossover (mating) between two parents to produce an offspring. """
    # Randomly select a crossover point
    crossover_point = random.randint(1, len(parent1) - 1)
    # Create offspring by combining the genes of the parents at the crossover point
    offspring = parent1[:crossover_point] + parent2[crossover_point:]
    # Display the crossover process and the resulting offspring
    print(f"Crossover result: {individual_to_string(offspring)} (from {individual_to_string(parent1)} x {individual_to_string(parent2)})")
    return offspring

def mutate(individual, mutation_rate):
    """ Performs mutation on an offspring at a given mutation rate. """
    for i in range(len(individual)):
        # Each gene (bit) has a chance to be flipped according to the mutation rate
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]  # Flip the bit
            # Display the mutation event
            print(f"Mutation: Bit at index {i} flipped in {individual_to_string(individual)}")
    return individual

def genetic_algorithm(population_size, individual_length, mutation_rate, generations):
    # Generate the initial population of random individuals
    population = [generate_individual(individual_length) for _ in range(population_size)]
    print("Initial population:")
    for ind in population:
        print(individual_to_string(ind))

    # Iteratively evolve the population over a number of generations
    for generation in range(generations):
        print(f"\n--- Generation {generation} ---")
        # Compute fitness for each individual in the population
        fitnesses = [compute_fitness(ind) for ind in population]

        new_population = []
        for _ in range(population_size):
            # Select parents for creating the next generation
            parent1, parent2 = select_parents(population, fitnesses)
            # Perform crossover between the selected parents to produce offspring
            offspring = crossover(parent1, parent2)
            # Perform mutation on the offspring
            offspring = mutate(offspring, mutation_rate)
            # Add the offspring to the new population
            new_population.append(offspring)
            print(f"Added offspring to new population: {individual_to_string(offspring)}")

        # Replace the old population with the new population for the next generation
        population = new_population
        print(f"New population at the end of generation {generation}:")
        for ind in population:
            print(individual_to_string(ind))

    # Identify the best individual in the final population based on fitness
    best_individual = max(population, key=compute_fitness)
    print("\nBest individual found after evolution:")
    return best_individual

# Set random seed for reproducibility
random.seed(42)

# Run the genetic algorithm with verbose output and detailed comments
best_individual = genetic_algorithm(6, 5, 0.3, 5)
print("Best individual:", individual_to_string(best_individual))
