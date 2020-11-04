from typing import List
from copy import copy
from random import shuffle
from collections import namedtuple

from templates import Gen as Schedule, Lesson, Classroom, Time, Teacher
from templates import l_pool, c_pool, t_pool, week_schedule, time_schedule, display_results


def run():
    DomainEl = namedtuple('DomainEl', 'day time room teacher')
    domain = []
    for day in week_schedule.keys():
        for time in time_schedule.keys():
            for room in c_pool:
                for teacher in t_pool:
                    domain.append(DomainEl(day, time, room, teacher))

    schedule = forward_checking(domain, l_pool)
    display_results(schedule)


def forward_checking(domain: list, pool: List[Lesson], schedule=Schedule([], [], []), previous_d=False):
    if len(pool) == 0:
        return schedule
    pool = copy(pool)
    shuffle(pool)
    shuffle(domain)
    lesson = pool.pop()
    for d in domain:
        if d == previous_d:
            pass
        if lesson.teacher == d.teacher and (not lesson.is_lecture or d.room.is_big):
            new_domain = clear_domain(domain, d.day, d.time, d.room, d.teacher)
            schedule.lessons.append(lesson)
            schedule.classrooms.append(d.room)
            schedule.times.append(Time(d.day, d.time))
            return forward_checking(new_domain, pool, schedule=schedule, previous_d=d)

    # step back
    if len(schedule.lessons):
        schedule.lessons.pop()
        schedule.classrooms.pop()
        schedule.times.pop()
        return forward_checking(domain, pool, schedule=schedule, previous_d=previous_d)


def clear_domain(domain: list, day: int, time: int, room: Classroom, teacher: Teacher):
    new_domain = []
    for d in domain:
        if not(d.day == day and d.time == time and (d.teacher == teacher or d.room == room)):
            new_domain.append(d)
    return new_domain


if __name__ == '__main__':
    run()
