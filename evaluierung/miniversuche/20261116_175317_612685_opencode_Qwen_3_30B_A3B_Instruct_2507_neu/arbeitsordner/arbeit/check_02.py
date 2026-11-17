def check_02():
    # Sollwert: True für x=1
    result = positiv(1)
    assert result is True, f"Fehler: positiv(1) = {result}, erwartet: True"
    print("Test 1 erfolgreich: positiv(1) = True")

    # Sollwert: False für x=0
    result = positiv(0)
    assert result is False, f"Fehler: positiv(0) = {result}, erwartet: False"
    print("Test 2 erfolgreich: positiv(0) = False")

    # Sollwert: False für x=-5
    result = positiv(-5)
    assert result is False, f"Fehler: positiv(-5) = {result}, erwartet: False"
    print("Test 3 erfolgreich: positiv(-5) = False")

    print("Alle Tests für positiv() erfolgreich.")