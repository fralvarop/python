def solution(S):
    # A single counter for left-right balance is better than two separate counters
    leftiness = 0
    workers = 0
    for item in S:
        if item == "L":
            leftiness += 1
        else:
            leftiness -= 1
        # Add one worker every time left and right shoes are balanced
        if leftiness == 0:
            workers += 1
    return workers
