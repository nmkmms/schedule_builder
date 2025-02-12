"""First place lessons of most busy teachers (affects more neighbours).

Power heuristics."""
from collections import defaultdict
import time

from templates import Gen as Schedule, Lesson, Classroom, Time
from templates import l_pool, c_pool, week_schedule, time_schedule, display_results
from minimum_remaining_values import run_heuristic


def run():
    counter = defaultdict(int)
    for lesson in l_pool:
        counter[lesson.teacher.name] += 1
    l_pool.sort(key=lambda l: counter[l.teacher.name])

    schedule = run_heuristic(l_pool)
    display_results(schedule)


if __name__ == '__main__':
    run()
