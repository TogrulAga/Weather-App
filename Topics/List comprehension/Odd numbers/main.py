digits = list(input())

odds = list(filter(lambda x: int(x) % 2 == 1, digits))

print(list(map(int, odds)))
