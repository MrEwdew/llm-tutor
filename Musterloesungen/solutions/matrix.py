from wypp import *

Matrix = list[list[float]]

# Multipliziert zwei Matrizen.
# Eine Matrix wird als verschachtelte Liste dargestellt, die äußere Liste repräsentiert
# die Zeilen, die inneren Liste sind die Spalteneinträge der jeweiligen Zeile.
# Multiplikation ist nur möglich, wenn A so viele Spalten wie B Zeilen hat.
# Eingabe: die beiden Matrizen
# Ergebnis: das Ergebnis der Multiplikation, eine Matrix
def matrixMult(a: Matrix, b: Matrix) -> Matrix:
    m = len(a)    # Anzahl Zeilen von a
    n = len(a[0]) # Anzahl Spalten von a und Anzahl Zeilen von b
    p = len(b[0]) # Anzahl Spalten von b
    if n != len(b):
        impossible(f'Kann eine {m}x{n} Matrix nicht mit einer {len(b)}x{p} Matrix multiplizieren')
    c = createZeroMatrix(m, p) # Ergebnismatrix c hat m Zeilen und p Spalten
    for i in range(m):
        for j in range(p):
            sum = 0
            for k in range(n):
                sum = sum + a[i][k] * b[k][j]
            c[i][j] = sum
    return c

# Erstellt ein Matrix mit lauter Nullen der gegeben Dimension
# Eingabe: die gewünschte Anzahl an Spalten und Zeilen
# Ergebnis: die Matrix
def createZeroMatrix(m: int, n: float) -> Matrix:
    c = []
    for i in range(m):
        row = [0 for j in range(n)]
        c.append(row)
    return c

check(createZeroMatrix(3, 2), [[0, 0], [0, 0], [0, 0]])

matrixD = [[3,2,1], [1,0,2]]
matrixE = [[1,2], [0,1], [4,0]]

check(matrixMult(matrixD, matrixE), [[7, 8], [9, 2]])
check(matrixMult(matrixE, matrixD), [[5, 2, 5], [1, 0, 2], [12, 8, 4]])

matrixF = [[1, 2], [2, 3]]
check(matrixMult(matrixE, matrixF), [[5, 8], [2, 3], [4, 8]])

