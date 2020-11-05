import time
import sys, os
import genetic, least_constraining_value, minimum_remaining_values, power_heuristic

ACCURACY = 4
OMIT_OUTPUT = True
NO_OF_TESTS = 5


def main():
    """Run imported algorithms and show statistics."""
    if OMIT_OUTPUT:
        sys.stdout = open(os.devnull, 'w')

    genetic_time, lcv_time, mrv_time, ph_time = [], [], [], []

    for _ in range(NO_OF_TESTS):
        now = time.time()
        genetic.run()
        genetic_time.append(time.time() - now)

        now = time.time()
        least_constraining_value.run()
        lcv_time.append(time.time() - now)

        now = time.time()
        minimum_remaining_values.run()
        mrv_time.append(time.time() - now)

        now = time.time()
        power_heuristic.run()
        ph_time.append(time.time() - now)

    if OMIT_OUTPUT:
        sys.stdout = sys.__stdout__

    algorithms = ['Genetic', 'Least constraining value',
                  'Minimum remaining values', 'Power heuristic']
    stats = [genetic_time, lcv_time, mrv_time, ph_time]

    for name, t in zip(algorithms, stats):
        avg_time = round(sum(t) / NO_OF_TESTS * 1000, ACCURACY)
        print(f"Statistics for {name} algorithm: {avg_time} ms.")


if __name__ == '__main__':
    main()
