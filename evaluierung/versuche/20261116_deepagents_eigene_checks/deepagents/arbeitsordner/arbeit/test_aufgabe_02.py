def test_positiv():
    assert positiv(1) == True
    assert positiv(0) == False
    assert positiv(-1) == False

if __name__ == '__main__':
    test_positiv()
    print('Test aufgabe_02 erfolgreich.')