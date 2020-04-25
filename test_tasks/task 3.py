def solution(S):
    # This operation is very similar to a very famous mathematical series, I just can't remember the author :_(

    # Remove leading zeroes
    S=S.lstrip('0')
    # If string is empty after trimming, it was just a (short '0' or long '0000') zero
    if S == '':
        return 0
    # '1' becomes our root case
    elif S == '1':
        return 1
    # If odd, remove one and repeat
    elif S[-1] == '1':
        return solution(S[0:-1] + '0') + 1
    # If even, divide by two, i.e., remove the last '0' and repeat
    else:
        return solution(S[0:-1]) + 1

