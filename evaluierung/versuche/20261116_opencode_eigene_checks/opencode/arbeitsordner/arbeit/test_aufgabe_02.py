def test_positiv():
    assert positiv(5) == True
    assert positiv(-1) == False
    assert positiv(0) == False
    assert positiv(100) == True

if __name__ == "__main__":
    test_positiv()
    print("All tests passed for positiv.")