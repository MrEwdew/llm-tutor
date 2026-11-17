def bar(i: int) -> int:
    x = bar(i - 1)
    return i + x

print(bar(4))
