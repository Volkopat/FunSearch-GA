BEGIN
    Generate the initial population
    Compute fitness of the population

    WHILE termination condition not met DO
        Selection: Select parents for reproduction
        Crossover: Create offspring by combining parts of parents
        Mutation: Mutate the offspring
        Compute fitness of the offspring
        Replace the old population with the offspring

    END WHILE

    Output the best solution
END