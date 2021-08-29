ls = list(map(int, input()))
print([sum(ls[:i]) for i in range(1, len(ls) + 1)])
