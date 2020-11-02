from random import choice, choices, randrange
from copy import deepcopy
from typing import List

from templates import Gen, Lesson, Classroom, Time, display_results
from templates import l_pool, c_pool, time_pool


START_POPULATION = 10
ELITE_POPULATION = 2
CHILDREN_PER_GEN = (START_POPULATION - ELITE_POPULATION) // ELITE_POPULATION
MAX_STEPS = 150


def create_population(lessons: List[Lesson], classrooms: List[Classroom], times: List[Time]) -> List[Gen]:
    """Create starting population."""
    population = []
    for _ in range(START_POPULATION):
        g_rooms = choices(classrooms, k=len(lessons))
        g_times = choices(times, k=len(lessons))
        population.append(Gen(lessons, g_rooms, g_times))

    return population


def heuristic(gen: Gen) -> int:
    """Value function for gen."""
    output = 0
    booked_rooms = set()
    teacher_times = set()
    for i in range(len(gen.lessons)):
        if gen.lessons[i].is_lecture and not gen.classrooms[i].is_big:
            output += 1
        teacher_times.add((gen.lessons[i].teacher, gen.times[i]))
        booked_rooms.add((gen.classrooms[i], gen.times[i]))
    output += (len(gen.lessons) - len(booked_rooms))
    output += (len(gen.lessons) - len(teacher_times))
    return output


def mutate(gen: Gen, classrooms: List[Classroom], times: List[Time]) -> Gen:
    """Make random mutations."""
    gen = deepcopy(gen)
    rand_class = randrange(0, len(gen.lessons))
    rand_time = randrange(0, len(gen.lessons))
    gen.classrooms[rand_class] = choice(classrooms)
    gen.times[rand_time] = choice(times)
    return gen


def children(gens: List[Gen], classrooms, times):
    new_pop = []
    for g in gens:
        for i in range(CHILDREN_PER_GEN):
            new_pop.append(mutate(g, classrooms, times))
    return new_pop


def run():
    """Run other functions & display results."""
    population = create_population(l_pool, c_pool, time_pool)

    steps = 0
    while heuristic(population[0]) and MAX_STEPS - steps:
        population.sort(key=heuristic)
        population = population[:ELITE_POPULATION]
        population += children(population, c_pool, time_pool)
        steps += 1

    solution = population[0]

    # display results for solution
    display_results(solution)


if __name__ == '__main__':
    run()
