def solution(S):
    # This formula corresponds to a very famous mathematical series, I just can't remember the author :_(
    V = int(S, 2)
    steps = 0
    while V > 0:
        if V % 2 == 0:
            V /= 2
        else:
            V -= 1
        steps += 1
    return steps
