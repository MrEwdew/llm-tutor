def test_quadrat():
    assert quadrat(2) == 4
    assert quadrat(0) == 0
    assert quadrat(-3) == 9

if __name__ == '__main__':
    test_quadrat()
    print('Test aufgabe_01 erfolgreich')