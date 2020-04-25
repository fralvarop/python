# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
import statistics

def solution(A):
    # If there is a statistical mode, USE IT!!
    try:
        goal = statistics.mode(A)
    # Otherwise, try any other number close to the average/mean (simply picking A[0] may fail)
    except:
        mean = statistics.mean(A)
        candidate_goal = round(mean)
        if candidate_goal in A:
            goal = candidate_goal
        else:
            goal = statistics.median(A)
    # Identify the opposite face
    opposite = 7 - goal
    # And now just count rotations per die and face!!
    rotations = 0
    for item in A:
        if (item == goal):
            pass
        elif (item == opposite):
            rotations += 2
        else:
            rotations += 1
    return rotations
