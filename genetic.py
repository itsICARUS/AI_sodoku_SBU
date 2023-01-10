# Python3 program to create target string, starting from
# random string using Genetic Algorithm

import random

# Number of individuals in each generation
POPULATION_SIZE = 500

# Valid genes
GENES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

tool = len(GENES)

part = 3

sudoku = []

max = 140

class __():
    def is_set(self):
        return True
running = __()


class Individual(object):
    '''
    Class representing individual in population
    '''

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls, gene_in):
        '''
        create random genes for mutation where gene_in is
        not 0
        '''
        global GENES, tool
        gene = []
        for i in range(tool):
            if gene_in[i]:
                gene.append(gene_in[i])
            else:
                gene.append(random.choice(GENES))
        return gene

    @classmethod
    def create_gnome(cls):
        '''
        create chromosome or string of genes
        '''
        global sudoku
        gnome = [cls.mutated_genes(sudoku[i]) for i in range(tool)]
        return gnome

    def mate(self, par2):
        '''
        Perform mating and produce new offspring
        '''

        global sudoku
        # chromosome for offspring
        child_chromosome = []
        for i, (gp1, gp2) in enumerate(zip(self.chromosome, par2.chromosome)):

            # random probability
            prob = random.random()

            # if prob is less than 0.45, insert gene
            # from parent 1
            if prob < 0.45:
                child_chromosome.append(gp1)

            # if prob is between 0.45 and 0.90, insert
            # gene from parent 2
            elif prob < 0.90:
                child_chromosome.append(gp2)

            # otherwise insert random gene(mutate),
            # for maintaining diversity
            else:
                prob = random.random()
                if prob < 0.45:
                    if prob < 0.225:
                        child_chromosome.append(self.partial_mutation(gp1, sudoku[i], 1))
                    else:
                        child_chromosome.append(self.partial_mutation(gp1, sudoku[i], 2))
                elif prob < 0.90:
                    if prob < 0.675:
                        child_chromosome.append(self.partial_mutation(gp2, sudoku[i], 1))
                    else:
                        child_chromosome.append(self.partial_mutation(gp2, sudoku[i], 2))
                else:
                    child_chromosome.append(self.mutated_genes(sudoku[i]))

        # create new Individual(offspring) using
        # generated chromosome for offspring
        return Individual(child_chromosome)

    def cal_fitness(self):
        '''
        Calculate fitness score, it is the number of
        characters in string which differ from target
        string.
        '''
        global tool, part
        fitness = 0
        # row fitness
        for i, gene in enumerate(self.chromosome):
            gene_set = set(gene)
            fitness += len(gene_set)
        # column fitness
        for i in range(tool):
            gene_set = set()
            for gene in self.chromosome:
                gene_set.add(gene[i])
            fitness += len(gene_set)
        # box fitness
        gene_sets = [[] for _ in range(part)]
        for i in range(tool):
            for j in range(tool):
                if not (j % part) and not (i % part):  # 00,03,06,30,33,36,60,63,66
                    # 66 box is 66 67 76 till 88 with length = 9
                    gene_sets[i // part].append(set())
                gene_sets[i // part][j // part].add(self.chromosome[i][j])
        for gss in gene_sets:
            for gs in gss:
                fitness += len(gs)
        return tool * tool * 3 - fitness  # because best fitness in this file is 0

    def partial_mutation(self, gp2, const, bin_1_or_2=1):
        global GENES, tool
        gene = []
        for i in range(len(gp2)):
            if const[i]:
                gene.append(const[i])
            else:
                prob = random.random()
                if prob < 0.4 * bin_1_or_2:
                    gene.append(random.choice(GENES))
                else:
                    gene.append(gp2[i])

        return gene


# Driver code
def runner(population):
    global max
    generation = 1
    found = False
    while not found and running.is_set() and generation<max:
        # sort the population in increasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness)

        # if the individual having the lowest fitness score i.e.
        # 0 then we know that we have reached to the target
        # and break the loop
        if population[0].fitness <= 0:
            found = True
            break

        # Otherwise generate new offsprings for new generation
        new_generation = []

        # Perform Elitism, that mean 10% of fittest population
        # goes to the next generation
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        # From 50% of fittest population, Individuals
        # will mate to produce offspring
        s = int((90 * POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        generation += 1
    print(f"found{found},generation{generation}")
    max += 10
    return population[0].chromosome, found


def main(sudoku_in):
    global POPULATION_SIZE
    global sudoku
    sudoku = sudoku_in
    ans = None
    found = False
    while running.is_set() and not found:
        # current generation
        population = []
        # create initial population
        for _ in range(POPULATION_SIZE):
            gnome = Individual.create_gnome()
            population.append(Individual(gnome))
        ans , found = runner(population)
    if found :
        print("1 ans is found :", ans)
        return ans
    pass


def find( return_dict, run, sudoku_in):
    global running
    running = run
    while run.is_set():
        ans = main(sudoku_in)
        if ans :
            return_dict["sudoku"] = ans
        run.clear()
