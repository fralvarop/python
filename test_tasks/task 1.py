def solution(A):
    rotations = []
    # We assess what would happen if we chose every single die as the goal
    for die in A:
        goal = die
        opposite = 7 - goal
        moves = 0
        # For the defined goal, calculate the distance (in moves) from it
        for item in A:
            if (item == goal):
                pass
            elif (item == opposite):
                moves += 2
            else:
                moves += 1
        # Collect all possible solutions
        rotations.append(moves)
    # Pick the minimum (as desired)
    return min(rotations)

