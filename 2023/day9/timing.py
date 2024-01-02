from timeit import default_timer as timer

def time_me(fn) -> None:
    try:
        start = timer()
        fn()
    except ValueError as err:
        print(err)
    else:
        end = timer()
        print(f"Ran for {end - start} seconds")