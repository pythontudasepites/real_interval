
from interval import Interval
from typing import Iterable, Literal
from random import triangular
from matplotlib import pyplot as plt

def relative_frequency(data: Iterable[int | float], a: int | float, b: int | float,
                       bins: int = 50, bin_repr_value: Literal['lower', 'upper', 'mid'] = 'lower'):
    """A data által kiadott és az [a, b] intervallumba eső valós számok relatív gyakoriságát adja 
    vissza egy szótárban, amelynek kulcsai az [a, b] intervallum bins számú részintervallumainak
    az alsó vagy felső végpontja, illetve az intervallum középértéke attól függően, hogy a 
    bin_repr_value milyen értékre van állítva.
    """
    frequencies = dict.fromkeys(Interval(a, b).split(bins), 0)
    total_data_points = 0
    for total_data_points, x in enumerate(data, 1):
        for interval in frequencies.keys():
            if x in interval:
                frequencies[interval] += 1
    if total_data_points:
        return {iv.reprval(bin_repr_value): freq / total_data_points
                for iv, freq in frequencies.items()}
    raise ValueError('A "data" argumentum legalább egy elemet kell, hogy kiadjon.')



# TESZT
# Háromszögeloszlású véletlen értékeket generálunk adott módusszal.
rand_seq = (triangular(-100, 100, 50) for _ in range(100000))
# Előállítjuk a relatív gyakoriságukat és ezt ábrázolva megnézzük, hogy
# mennyire közelíti a háromszögeloszlást.
rel_freq = relative_frequency(rand_seq, -100, 100)


# A relatív gyakoriság ábrázolása.
xs = rel_freq.keys()
ys = rel_freq.values()
plt.plot(xs, ys, '.')
plt.title('Háromszögeloszlás')
plt.legend(loc='upper left', labels=['triangular(-100, 100, 50)'])
plt.xlabel('Véletlen változó értéke')
plt.ylabel('Relatív gyakoriság')
plt.text(60, 0.038, "módusz = 50")
plt.show()


