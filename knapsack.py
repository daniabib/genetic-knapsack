from __future__ import annotations

from dataclasses import dataclass
from random import randint
import numpy as np

WEIGHT_LIMIT = 55


@dataclass
class Item:
    id: int
    value: int
    weight: int

    def __lt__(self, other: Item):
        return self.id < other.id


class Individual:
    def __init__(self, genome_length: int) -> None:
        self.genome: str = ""
        for _ in range(genome_length):
            self.genome += str(randint(0, 1))
        self.fitness: int = 0

    def __repr__(self) -> str:
        if hasattr(self, "select_prob"):
            return f"Individual({self.genome}, fitness={self.fitness}, select_prob={self. select_prob :.3f})"
        return f"Individual({self.genome}, fitness={self.fitness})"

    def calculate_fitness(
            self,
            items: list[Item],
            max_weight: int) -> None:
        score = 0
        for i, item in enumerate(items):
            if self.genome[i] == "1":
                score += item.value
        if score > max_weight:
            self.fitness = 0
        else:
            self.fitness = score

    def calculate_selection_prob(self, pop_fitness: int):
        self.select_prob = self.fitness / pop_fitness

    def mutation(self, mutation_prob: int = 0.05):
        """Applies flip bit mutation"""
        if np.random.random() < mutation_prob:
            chosen_gene = np.random.choice(len(self.genome))
            pre_mutation_left_gene = self.genome[:chosen_gene]
            pre_mutation_right_gene = self.genome[chosen_gene + 1:]
            mutate_gene = "1" if self.genome[chosen_gene] == "0" else "0"
            self.genome = pre_mutation_left_gene + mutate_gene + pre_mutation_right_gene


class Population:
    def __init__(
            self,
            individuals: list[Individual],
            items: list[Item]) -> None:
        assert len(individuals[0].genome) == len(items)
        self.individuals = individuals
        self.items = sorted(items)

    def calc_pop_fitness(self, items: list[Item], max_weight: int):
        for individual in self.individuals:
            individual.calculate_fitness(items, max_weight)

    def selection(self) -> None:
        """Uses fitness proportionate selection (FPS)

        Each time the wheel is turned, the selection point is used to choose a single individual from the entire population. The wheel is then turned again to select the next individual until we have enough individuals selected to fill the next generation. As a result, the same individual can be picked several times.
        """
        total_fitness = sum(
            individual.fitness for individual in self.individuals)
        probs = []
        for individual in self.individuals:
            individual.calculate_selection_prob(total_fitness)
            probs.append(individual.select_prob)
        assert np.isclose(sum(probs), 1.0, rtol=1e-05,
                          atol=1e-08, equal_nan=False)
        chosen_inds = []
        for _ in range(len(self.individuals)):
            chosen_inds.append(np.random.choice(
                self.individuals, size=1, p=probs)[0])
        self.individuals = chosen_inds

    def crossover(self, crossover_prob: int = 0.55):
        """Uses single-point crossover"""

        genome_length = len(self.individuals[0].genome)
        for i in range(0, len(self.individuals) - 1, 2):
            print(i)
            if np.random.random() < crossover_prob:
                crossover_point = np.random.randint(0, genome_length - 1)
                # print("Crossover point:", crossover_point)
                # print("Parent 1:", self.individuals[i].genome)
                # print("Parent 2:", self.individuals[i+1].genome)
                copied_gene = self.individuals[i].genome[crossover_point:]
                self.individuals[i].genome = self.individuals[i].genome[:crossover_point] + \
                    self.individuals[i+1].genome[crossover_point:]

                self.individuals[i+1].genome = self.individuals[i+1].genome[:crossover_point] + \
                    copied_gene
                # print("Children 1:", self.individuals[i].genome)
                # print("Children 2:", self.individuals[i+1].genome)

    def __repr__(self) -> str:
        return f"Population(individuals={self.individuals})"


def generate_items(n: int, random: bool = False) -> list[Item]:
    if random:
        return [Item(i, randint(1, 10), randint(1, 10)) for i in range(n)]
    return [Item(i, i+1, i+1) for i in range(n)]


def create_initial_population(
        number_individuals: int,
        genome_lenght: int,
        items: list[Item]) -> Population:
    return Population([Individual(genome_lenght)
                       for _ in range(number_individuals)], items)


if __name__ == "__main__":
    items = generate_items(10, random=True)

    init_pop = create_initial_population(13, 10, items)
    print(init_pop)

    init_pop.calc_pop_fitness(items, WEIGHT_LIMIT)
    # print(init_pop)

    init_pop.selection()
    # print(init_pop)
    init_pop.crossover(crossover_prob=.9999)

