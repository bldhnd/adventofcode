from timeit import default_timer as timer
import problem2


if __name__ == "__main__":
    start = timer()
    problem2.problem_2()
    end = timer()
    print(f"Ran for {end - start} seconds")
