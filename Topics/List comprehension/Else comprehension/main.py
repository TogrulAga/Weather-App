# the following line reads the list from the input, do not modify it, please
old_list = [int(num) for num in input().split()]

binary_list = list(map(lambda x: 1 if x > 0 else 0, old_list))
print(binary_list)
