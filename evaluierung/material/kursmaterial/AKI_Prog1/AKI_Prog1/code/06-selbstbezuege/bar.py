def bar(i: int) -> int:
    if i == 0:
        return 0
    else:
        x = bar(i - 1)
        return i + x

print(bar(4))
