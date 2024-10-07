
from interval import Interval, IntervalType
from collections import Counter
from itertools import repeat, chain
from statistics import median, mean

# Saját jogon járó nyugdíjban és ellátásban részesülők a teljes ellátás összege szerint, 2024 január.

# Osztályközök (nyugdíjintervallumok) és a gyakoriságok (hány fő esik az intervallumba).
pension_groups1 = Interval(0, 40_000, IntervalType.OPEN).split(1)
pension_groups2 = Interval(40_000, 500_000, IntervalType.RIGHT_OPEN).split(23)
pension_groups3 = Interval(500_000, 600_000, IntervalType.RIGHT_OPEN).split(1)
pension_groups4 = Interval(600_000, 3000_000, IntervalType.CLOSED).split(1)

frequencies = (20_523,
               40_322, 68_253, 68_829, 116_958, 188_143, 208_540, 241_008, 213_268,
               184_412, 160_182, 130_811, 107_759, 91_153, 76_771, 64_222, 52_959,
               42_793, 34_816, 28_423, 23_472, 19_135, 15_432, 12_790,
               35_912,
               24_475)

print('''Saját jogon járó nyugdíjban és ellátásban részesülők (fő)
a teljes ellátás összege szerint (Ft), 2024 január.''')

# Az egymást követő osztályközök összefűzése.
pension_groups = chain(pension_groups1, pension_groups2, pension_groups3, pension_groups4)

# Osztályközös gyakoriságtábla elkészítése.
grouped_frequency_table = Counter(dict(zip((iv for iv in pension_groups), frequencies)))

# A nyugdíjintervallumok és ezekbe eső ellátásban részedülők számának kiírása.
print(*(f'{str(pension_group):21}: {head_count:>7}'
        for pension_group, head_count in sorted(grouped_frequency_table.most_common())), sep='\n')

# Az osztályközöket képviselő középértékek és gyakoriságok megfeleltetése.
midpoint_frequency_table = Counter({iv.reprval('mid'): fr for iv, fr in grouped_frequency_table.items()})

print('Becsült átlag nyugdíj és ellátás: {0:_g} Ft'.format(mean(midpoint_frequency_table.elements())))
print('Becsült medián nyugdíj és ellátás: {0:_g} Ft'.format(median(midpoint_frequency_table.elements())))




# Források:
# https://www.ksh.hu/stadat_files/szo/hu/szo0035.html
# https://www.ksh.hu/s/helyzetkep-2023/#/kiadvany/nyugdijak-es-egyeb-ellatasok/
# sajat-jogon-jaro-nyugdijban-es-ellatasban-reszesulok-szama-nemek-es-a-teljes-ellatas-osszege-szerint-2024-januar
# https://forbes.hu/penz/nyugdij-emeles-reform-2024/


































