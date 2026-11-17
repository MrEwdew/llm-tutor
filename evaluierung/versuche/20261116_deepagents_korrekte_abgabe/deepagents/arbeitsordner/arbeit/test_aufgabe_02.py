def test_positiv():
    assert positiv(5) == True
    assert positiv(-1) == False
    assert positiv(0) == False

test_positiv()