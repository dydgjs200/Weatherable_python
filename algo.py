# 30의 배수이려면 맨 끝자리에 0이 붙어있어야함.
# 맨 끝자리를 제외한 값에서, 각 자리의 합이 3의 배수여야함.
# boj 10610

num = list(map(int, input()))

if 0 not in num:
    print(-1)
else:
    num.sort(reverse=True)

    if sum(num) % 3 != 0:
        print(-1)
    else:
        print("".join(map(str, num)))