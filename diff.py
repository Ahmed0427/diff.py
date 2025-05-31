#!/usr/bin/env python3

import sys

def read_file(path):
    with open(path) as f:
        lines = f.read().splitlines()
        while lines and lines[-1] == "":
            lines.pop()

        return lines

ADD = 'A'
SUBST = 'S'
IGNORE = 'I'
REMOVE = 'R'

def lev_dist_actions(lines1, lines2):
    n, m = len(lines1), len(lines2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    actions = [['X'] * (m + 1) for _ in range(n + 1)]

    dp[0][0] = 0
    actions[0][0] = IGNORE

    for i in range(1, n + 1):
        dp[i][0] = i
        actions[i][0] = REMOVE

    for j in range(1, m + 1):
        dp[0][j] = j
        actions[0][j] = ADD

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if lines1[i - 1] == lines2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                actions[i][j] = IGNORE
            else:

                dp[i][j] = dp[i - 1][j];
                actions[i][j] = REMOVE

                if dp[i][j] > dp[i][j - 1]:
                    dp[i][j] = dp[i][j - 1]
                    actions[i][j] = ADD


                if dp[i][j] > dp[i - 1][j - 1]:
                    dp[i][j] = dp[i - 1][j - 1];
                    actions[i][j] = SUBST

                dp[i][j] += 1


    trace = []
    i, j = n, m
    while i and j:
        action = actions[i][j]
        if action == ADD:
            j -= 1
            trace.append((action, lines2[j]))
        elif action == REMOVE:
            i -= 1
            trace.append((action, lines1[i]))
        elif action == SUBST:
            i -= 1
            j -= 1
            trace.append((action, lines1[i], lines2[j]))
        elif action == IGNORE:
            i -= 1
            j -= 1
            trace.append((action, lines1[i]))
        else:
            assert False, "Unreachable"

    while i:
        action = actions[i][j]
        i -= 1
        trace.append((action, lines1[i]))

    while j:
        action = actions[i][j]
        j -= 1
        trace.append((action, lines2[j]))

    return reversed(trace)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1> <file2>")
        exit(1)

    lines1 = read_file(sys.argv[1])
    lines2 = read_file(sys.argv[2])

    for action in lev_dist_actions(lines1, lines2):
        if action[0] == 'I':
            print(' ' + action[1])
        elif action[0] == 'A':
            print('\033[32;1m' + '+' + action[1] + '\033[0m')
        elif action[0] == 'R':
            print('\033[31;1m' + '-' + action[1] + '\033[0m')
        elif action[0] == 'S':
            print('\033[31;1m' + '-' + action[1] + '\033[0m')
            print('\033[32;1m' + '+' + action[2] + '\033[0m')
        else:
            assert False, "Unreachable"
