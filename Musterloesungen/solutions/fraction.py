from __future__ import annotations
from wypp import *
from math import gcd

@record
class Fraction:
    numerator: int
    denominator: int
    def __post_init__(self: Fraction):
        if self.denominator == 0:
            raise ValueError('ungültiger Bruch')
    def __add__(self: Fraction, other: Fraction) -> Fraction:
        newDenominator = self.denominator * other.denominator
        newNumerator = self.numerator * other.denominator + other.numerator * self.denominator
        return Fraction(newNumerator, newDenominator).cancel()
    def __lt__(self: Fraction, other: Fraction) -> bool:
        return self.numerator * other.denominator < other.numerator * self.denominator
    def cancel(self: Fraction) -> Fraction:
        n = self. numerator
        d = self.denominator
        isPositive = True
        if (n < 0 and d > 0) or (n > 0 and d < 0):
            isPositive = False
        n = abs(n)
        d = abs(d)
        x = gcd(n, d)
        n = n // x
        d = d // x
        if not isPositive:
            n = -1 * n
        return Fraction(n, d)


dreiViertel = Fraction(3, 4)
zweiFünftel = Fraction(2, 5)

beispiel1 = Fraction(2, -6)
check(beispiel1.cancel(), Fraction(-1, 3))

beispiel2 = Fraction(-15, -5)
check(beispiel2.cancel(), Fraction(3, 1))

beispiel3 = Fraction(8, 10)
check(beispiel3.cancel(), Fraction(4, 5))

check(dreiViertel + zweiFünftel, Fraction(23, 20))

check(dreiViertel < zweiFünftel, False)
