from dataclasses import dataclass
from random import randint

WEIGHT_LIMIT = 55


@dataclass
class Item:
    id: int
    value: int
    weight: int


class Individual:
    def __init__(self, genome_length: int) -> None:
        self.genome: str = ""
        for _ in range(genome_length):
            self.genome += str(randint(0, 1))
        self.fitness: int = 0

    def __repr__(self) -> str:
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


@dataclass
class Population:
    individuals: list[Individual]

    def calc_pop_fitness(self, items: list[Item], max_weight: int):
        for individual in self.individuals:
            individual.calculate_fitness(items, max_weight)


def generate_items(n: int, random: bool = False) -> list[Item]:
    if random:
        return [Item(i, randint(1, 10), randint(1, 10)) for i in range(n)]
    return [Item(i, i+1, i+1) for i in range(n)]


def create_initial_population(
        number_individuals: int,
        genome_lenght: int) -> Population:
    return Population([Individual(genome_lenght)
                       for _ in range(number_individuals)])


if __name__ == "__main__":
    items = generate_items(10)
    # print(items)

    random_items = generate_items(10, random=True)
    # print(random_items)

    ind = Individual(10)
    # print(ind)

    init_pop = create_initial_population(5, 10)
    print(init_pop)
    init_pop.calc_pop_fitness(random_items, WEIGHT_LIMIT)
    print(init_pop)
    # print(calculate_fitness(ind, LIMIT, random_items))

    ind.calculate_fitness(items, WEIGHT_LIMIT)
    # print(ind)

    # ind2 = Individual(10)
    # ind2.genome = "1111111111"
    # print(ind2)
    # ind2.calculate_fitness(items, WEIGHT_LIMIT)
    # print(ind2)
