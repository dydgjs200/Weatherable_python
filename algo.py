# boj 6603
from itertools import combinations

while True:
    lis = list(map(int, input().split(" ")))

    if lis[0] == 0:
        break

    com = combinations(lis[1:], 6)

    for c in com:
        print(*c)

    print()