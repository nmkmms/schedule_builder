from random import choice, choices, randrange
from collections import namedtuple
from copy import deepcopy
from typing import List


START_POPULATION = 10
ELITE_POPULATION = 2
CHILDREN_PER_GEN = (START_POPULATION - ELITE_POPULATION) // ELITE_POPULATION
MAX_STEPS = 150

# dicts for better output
week_schedule = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
time_schedule = {1: "8:30-9:50", 2: "10:00-11:20", 3: "11:40-13:00", 4: "13:30-14:50", 5: "15:00-16:20"}

# Defining and describing classes
Classroom = namedtuple("Lesson", "building room is_big")
Classroom.__repr__ = lambda c: f"{c.building}-{c.room} ({'big' if c.is_big else 'small'})"
Classroom.building.__doc__ += "Number of building."
Classroom.room.__doc__ += "Number of room."
Classroom.is_big.__doc__ += "if True -> suitable for both lectures and seminars, if False -> only for seminars."

Time = namedtuple("Time", "weekday number")
Time.__repr__ = lambda t: f"{week_schedule[t.weekday]}({time_schedule[t.number]})"
Time.weekday.__doc__ += "Number of weekday (according to week_schedule)."
Time.number.__doc__ += "Number of lesson (according to time_schedule)."

Teacher = namedtuple("Teacher", "name")
Teacher.__repr__ = lambda t: f"Teacher({t.name})"
Teacher.name.__doc__ += "Name of teacher."

Subject = namedtuple("Subject", "name")
Subject.__repr__ = lambda s: f"Subject({s.name})"
Subject.name.__doc__ += "Name of subject."

Group = namedtuple("Group", "id")
Group.__repr__ = lambda g: f"Group({g.id})"
Group.id.__doc__ += "Group id."

Lesson = namedtuple("Lesson", "teacher subject group is_lecture per_week")
Lesson.__repr__ = lambda l: f"{l.teacher}:{l.subject}:{l.group}:" \
                            f"{'Lecture' if l.is_lecture else 'Seminar'}:{l.per_week}/week"
Lesson.teacher.__doc__ += "Teacher object."
Lesson.subject.__doc__ += "Subject object."
Lesson.group.__doc__ += "Group object or objects."
Lesson.is_lecture.__doc__ += "if True -> it is a lecture, if False -> it is a seminar."
Lesson.per_week.__doc__ += "Number of lessons per week."

Gen = namedtuple("Gen", "lessons classrooms times")
Gen.__doc__ += "1st chromosome is mapping lessons-classrooms, second is mapping lessons-times."


def gen_repr(g: Gen):
    output = ""
    for i in range(len(g.lessons)):
        output += f"{g.lessons[i]},   {g.classrooms[i]},   {g.times[i]}\n"
    return output


Gen.__repr__ = lambda g: gen_repr(g)

# classrooms pool
c_pool = [
    Classroom(1, 101, True), Classroom(1, 113, False), Classroom(1, 210, False),
    Classroom(3, 215, False), Classroom(3, 313, True)
]

# time (schedule) pool
time_pool = [Time(w, n) for w in range(1, 6) for n in range(1, 6)]

# teachers pool
t_pool = [Teacher(name) for name in
                 ("Albert Smith", "Evan Rocks", "Jeremy Yang", "Anny Flint", "Bob Jacoby", "Terence McKenna", "Steve Jobs")]
# subjects pool
s_pool = [Subject(name) for name in
                 ("AI", "Topology", "Probability theory", "Network basics", "Optimisation methods", "Math analysis", "Java")]
# groups poll
g_pool = [Group(id) for id in
                 ("AI-1", "AI-2", "TP-1", "TP-2", "PT-1", "PT-2", "NB-1", "OM-1", "OM-2", "MA-1", "MA-2", "J-1")]

# lessons pool
l_pool = [
    # AI lessons
    Lesson(t_pool[0], s_pool[0], g_pool[0:2], True, 1),
    Lesson(t_pool[0], s_pool[0], g_pool[0], False, 1),
    Lesson(t_pool[0], s_pool[0], g_pool[1], False, 1),
    # Topology
    Lesson(t_pool[1], s_pool[1], g_pool[2:4], True, 1),
    Lesson(t_pool[1], s_pool[1], g_pool[2], False, 1),
    Lesson(t_pool[1], s_pool[1], g_pool[3], False, 1),
    # Probability theory
    Lesson(t_pool[2], s_pool[2], g_pool[4:6], True, 1),
    Lesson(t_pool[2], s_pool[2], g_pool[4], False, 2),
    Lesson(t_pool[3], s_pool[2], g_pool[5], False, 2),
    # Networks basics
    Lesson(t_pool[4], s_pool[3], g_pool[6], True, 1),
    Lesson(t_pool[5], s_pool[3], g_pool[6], False, 1),
    # Optimisation methods
    Lesson(t_pool[6], s_pool[4], g_pool[7:9], True, 1),
    Lesson(t_pool[6], s_pool[4], g_pool[7], False, 2),
    Lesson(t_pool[6], s_pool[4], g_pool[8], False, 2),
    # Math analysis
    Lesson(t_pool[1], s_pool[5], g_pool[9:11], True, 1),
    Lesson(t_pool[1], s_pool[5], g_pool[9], False, 2),
    Lesson(t_pool[1], s_pool[5], g_pool[10], False, 2),
    # Java
    Lesson(t_pool[0], s_pool[6], g_pool[11], True, 2),
    Lesson(t_pool[0], s_pool[6], g_pool[11], False, 1), 
]


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


population = create_population(l_pool, c_pool, time_pool)

steps = 0
while heuristic(population[0]) and MAX_STEPS - steps:
    population.sort(key=heuristic)
    population = population[:ELITE_POPULATION]
    population += children(population, c_pool, time_pool)
    steps += 1

solution = population[0]

# display results for solution
for day in week_schedule.keys():
    print('\n' + '=' * 100)
    print(f"{week_schedule[day].upper()}")
    for time in time_schedule.keys():
        print('\n\n' + time_schedule[time])
        for c in c_pool:
            print(f'\n{c}', end='\t\t')
            for i in range(len(solution.lessons)):
                # print(day, time, c.building, c.room)
                if solution.times[i].weekday == day and solution.times[i].number == time and \
                        solution.classrooms[i].building == c.building and solution.classrooms[i].room == c.room:
                    print(solution.lessons[i], end='')

print('\n' + '=' * 100)
print(f'Total generations: {steps}')
