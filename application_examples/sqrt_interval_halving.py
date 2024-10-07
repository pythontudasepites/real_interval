
from interval import Interval
from math import isclose

def sqrt(x) -> float:
    """Az x négyzetgyökével tér vissza. A számítás intervallumfelezéses eljárással történik."""

    if x < 0:
        raise ValueError('Az argumentum nem lehet negatív szám.')
    
    current_interval = Interval(0, 1 if (0 <= x < 1) else x)
    
    while not isclose((middle_point := current_interval.midpoint()) ** 2, x, rel_tol=1e-15):
        
        lower_half, upper_half = current_interval.split(2)
        
        if middle_point ** 2 > x:
            current_interval = lower_half
        else:
            current_interval = upper_half
           
    return middle_point

# TESZT

print('Négyzetgyök 2 =', sqrt(2))        # Négyzetgyök 2 = 1.414213562373095
print('Négyzetgyök 0.75 =', sqrt(0.75))  # Négyzetgyök 0.75 = 0.8660254037844384

# Egész értékek négyzetgyökének pontosságvizsgálata.
for n in range(10000):
    if abs(sqrt(n) - pow(n, 0.5)) > 1e-13:
        print(n, y := sqrt(n), sqrt2 := pow(n, 0.5), abs(y - sqrt2))
# Eredmény: A megadott értéktartományban és abszolút hibahatáron belül egyezik a pow() függvénnyel számítottal.

# Egynél kisebb értékek négyzetgyökének pontosságvizsgálata.
s = 0.0001
for n in range(10000):
    if abs(sqrt(n * s) - pow(n * s, 0.5)) > 1e-15:
        print(n * s, y := sqrt(n*s), sqrt2 := pow(n * s, 0.5), abs(y - sqrt2))
# Eredmény: A megadott értéktartományban és abszolút hibahatáron belül egyezik a pow() függvénnyel számítottal.


