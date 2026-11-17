def check_01():
    # Sollwert: 25 für x=5
    result = quadrat(5)
    assert result == 25, f"Fehler: quadrat(5) = {result}, erwartet: 25"
    print("Test 1 erfolgreich: quadrat(5) = 25")

    # Sollwert: 0 für x=0
    result = quadrat(0)
    assert result == 0, f"Fehler: quadrat(0) = {result}, erwartet: 0"
    print("Test 2 erfolgreich: quadrat(0) = 0")

    # Sollwert: 1 für x=-1
    result = quadrat(-1)
    assert result == 1, f"Fehler: quadrat(-1) = {result}, erwartet: 1"
    print("Test 3 erfolgreich: quadrat(-1) = 1")

    print("Alle Tests für quadrat() erfolgreich.")