import json
import genetic
import multiprocessing

# *** you can change everything except the name of the class, the act function and the problem_data ***


def genetic_caller(problem_data):
    sudoku = problem_data["sudoku"]

    # use parallel processes for finding correct sudoku
    processes = []
    manager = multiprocessing.Manager()
    return_code = manager.dict()
    run = manager.Event()
    run.set()  # We should keep running.
    for i in range(5):
        process = multiprocessing.Process(
            target=genetic.find, args=( return_code, run, sudoku)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    return return_code


class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):
        # ^^^ DO NOT change the solve function above ***

        problem_data = json.loads(problem)
        # ^^^ DO NOT change the problem_data above ***
        # TO DO implement your code here
        ans_pdic = genetic_caller(problem_data)
        value = ans_pdic["sudoku"]
        ans = {"sudoku": value }
        finished = json.dumps(ans)
        # finished is the solved version
        return finished
