from aufgabe_01 import quadrat

def test_quadrat():
    assert quadrat(2) == 4
    assert quadrat(-3) == 9
    assert quadrat(0) == 0
    assert quadrat(1) == 1

if __name__ == "__main__":
    test_quadrat()
    print("All tests passed for quadrat.")