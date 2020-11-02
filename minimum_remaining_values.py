"""First place lectures, then seminars (Minimum remaining values)."""
from random import shuffle
from templates import Gen as Schedule, Lesson, Classroom, Time
from templates import l_pool, c_pool, week_schedule, time_schedule, display_results


def run():
    """Run & display results."""
    # sort lessons pool (first lectures)
    l_pool.sort(key=lambda l: 0 if l.is_lecture else 1)

    schedule = Schedule([], [], [])

    # make it a little bit funnier
    week_days = list(week_schedule.keys())
    shuffle(week_days)
    times = list(time_schedule.keys())
    shuffle(times)

    for lesson in l_pool:
        found = False
        for day in week_days:
            if found: break
            for time in times:
                if found: break
                for room in c_pool:
                    duplicate = False
                    for i in range(len(schedule.lessons)):
                        # if room is booked at this time or teacher is busy
                        if (schedule.times[i].weekday == day and schedule.times[i].number == time and \
                            schedule.classrooms[i].building == room.building) and \
                                (schedule.classrooms[i].room == room.room or schedule.lessons[i].teacher.name == lesson.teacher.name):
                            duplicate = True
                    if duplicate: continue
                    if found: break
                    if not lesson.is_lecture or room.is_big:
                        chosen_time = Time(day, time)
                        classroom = Classroom(room.building, room.room, room.is_big)
                        found = True
                        schedule.times.append(chosen_time)
                        schedule.classrooms.append(classroom)
                        schedule.lessons.append(lesson)

    display_results(schedule)
    assert len(schedule.lessons) == len(l_pool), "Didn't go well"


if __name__ == '__main__':
    run()
