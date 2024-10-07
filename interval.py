
from __future__ import annotations
import sys
from typing import Literal, Iterator
from itertools import pairwise, chain
from math import isclose
from enum import Enum
from collections import namedtuple

assert sys.version_info > (3, 9)  # Python 3.10+ szükséges.

class IntervalType(Enum):
    """Konstansok a különböző intervallum típusokhoz."""
    OPEN = (0, 0)  # Mindkét oldalon nyitott.
    LEFT_OPEN = (0, 1)  # Bal oldalon nyitott és jobb oldalon zárt.
    RIGHT_OPEN = (1, 0)  # Jobb oldalon nyitott és bal oldalom zárt.
    CLOSED = (1, 1)  # Mindkét oldalon zárt.

IType = IvType = IntervalType

IntervalEndpoint = namedtuple('IntervalEndpoint', 'value flag')
Endpoints = namedtuple('Endpoints', 'lower upper')

class Interval:
    """Egy valós értékkészletű korlátos intervallumot modellez."""

    def __init__(self, lower_endpoint_value: int | float, upper_endpoint_value: int | float, type: IntervalType = IntervalType.CLOSED):
        """Egy valós értékkészletű intervallumot meghatározza a két végpontja (lower_endpoint_value, upper_endpoint_value), amelyek közül
        a felső (jobb oldali) nagyobb, mint az alsó (bal oldali), és az, hogy a végeken nyitott vagy zárt. Ez utóbbi az
        intervallum típusát határozza meg, amelyet a type argumentummal lehet megadni az IntervalType felsorolástípus példányaival.
        Ezek a lehetséges kombinációkhoz (két oldalon zárt, két oldalon nyitott, bal oldalon nyitott és jobb oldalon zárt, valamint
        jobb oldalon nyitott és bal oldalon zárt) adnak egy-egy szimbólikus konstanst. Ezek mindegyikének értéke egy kételemű
        tuple, amely elemek rendre a bal oldal és jobb oldal nyitottságát, illetve zártságát mint bináris információt jelzik.
        Az érték 0, ha az adott oldalon az intervallum nyitott, és 1, ha zárt. Ezeket, mint a végpontokra jellemző jelzőket az
        Interval példány flags attribútumában tároljuk el.
        Ha egy adott végponton zárt az intervallum, akkor a végpont értéke az intervallum értékkészletébe beletartozik, nyitott esetben nem.
        Műveletek eredményeként kiadódhat olyan elfajult intervallum, amelynek egy eleme van, vagyis az alsó és felső végpontok azonosak.
        Ez megengedett ebben a modellben. Ellenben az üres, elemet nem tartalmazó intevallum nem értelmezett. Ha egy műveletből ilyen
        adódna, akkor None lesz az eredmény.
        """
        if lower_endpoint_value > upper_endpoint_value:
            raise ValueError('Upper endpoint should be greater than lower endpoint.')

        self._lower_endpoint, self._upper_endpoint = lower_endpoint_value, upper_endpoint_value
        self._type: IntervalType = type
        self._flags: tuple = type.value
        self.endpoints = Endpoints(IntervalEndpoint(lower_endpoint_value, self._flags[0]), IntervalEndpoint(upper_endpoint_value, self._flags[1]))

    @property
    def lower_endpoint(self) -> int | float:
        return self._lower_endpoint

    @property
    def upper_endpoint(self) -> int | float:
        return self._upper_endpoint

    @property
    def type(self) -> IntervalType:
        return self._type

    @property
    def flags(self) -> tuple:
        """Az alsó és felső végpontok nyitott vagy zárt jellegét leíró kételemű tuple.
        Ha az intervallum az adott végponton nyitott, akkor az érték 0, ha zárt, akkor 1.
        """
        return self._flags

    def __repr__(self):
        return '{}({}, {}, {})'.format(type(self).__name__, self.lower_endpoint, self.upper_endpoint, self.type)

    def __str__(self):
        brackets = {IntervalType.OPEN: (chr(0x2e28), chr(0x2e29)),
                    IntervalType.LEFT_OPEN: (chr(0x2e28), chr(0x27E7)),
                    IntervalType.RIGHT_OPEN: (chr(0x27E6), chr(0x2e29)),
                    IntervalType.CLOSED: (chr(0x27E6), chr(0x27E7))}
        return '{}{}, {}{}'.format(brackets[self.type][0], self.lower_endpoint, self.upper_endpoint, brackets[self.type][1])

    @classmethod
    def from_endpoint_values_and_flags(cls, lower_endpoint_value, upper_endpoint_value,
                                       lower_endpoint_flag: Literal[0, 1], upper_endpoint_flag: Literal[0, 1]) -> Interval:
        """Új Interval példányt hoz létre a végpontok, valamint a végpontok nyitottságát vagy zártságát
        jelző 0 vagy 1 értékek alapján.
        """
        return cls(lower_endpoint_value, upper_endpoint_value, IntervalType((lower_endpoint_flag, upper_endpoint_flag)))

    @classmethod
    def from_endpoints(cls, lower_endpoint: IntervalEndpoint, upper_endpoint: IntervalEndpoint) -> Interval:
        """Új Interval példányt hoz létre a végpontobjektumok alapján."""
        return cls.from_endpoint_values_and_flags(lower_endpoint.value, upper_endpoint.value, lower_endpoint.flag, upper_endpoint.flag)

    @staticmethod
    def _eq(num1: float, num2: float) -> bool:
        """Segédfüggvény két valós szám egyenlőségvizsgálatához."""
        return isclose(num1, num2, rel_tol=1e-15)

    def __eq__(self, other) -> bool:
        """Igaz értékkel tér vissza, ha a self és other egyenlő. Ezek akkor egyenlőek, ha az azonos oldalakon
        végpontjaik értéke egyenlő, és zártság/nyitottság tekintetében megegyeznek, vagyis értékkészletük azonos.
        """
        if not isinstance(other, Interval):
            return NotImplemented
        return self.type == other.type and (self._eq(self.lower_endpoint, other.lower_endpoint) and
                                            self._eq(self.upper_endpoint, other.upper_endpoint))

    def __hash__(self):
        return hash((*self.endpoints, *self.flags))

    def __lt__(self, other):
        """Igaz értékkel tér vissza, ha a self kisebb, mint other. A self akkor kisebb, mint other, ha
        self minden értéke, beleértve a végpontokat is, kisebb az other minden értékénél.
        """
        if not isinstance(other, Interval):
            return NotImplemented
        # Ahhoz, hogy a self kisebb legyen, mint other a következő feltételek valamelyikének kell teljesülni.
        # Ha a self felső végpontja kisebb, mint az other alsó végpontja.
        cond1 = self.upper_endpoint < other.lower_endpoint
        # Ha a self felső végpont és az other alsó végpont egyenlő és ezen oldalakon bármelyik intervallum nyitott.
        cond2 = self._eq(other.lower_endpoint, self.upper_endpoint) and (0 in (other.flags[0], self.flags[1]))
        return cond1 or cond2

    def __le__(self, other) -> bool:
        """Igaz értékkel tér vissza, ha a self kisebb vagy egyenlő, mint other."""
        if not isinstance(other, Interval):
            return NotImplemented
        return (self < other) or (self == other)

    def __contains__(self, value: int | float) -> bool:
        """Igaz értékkel tér vissza, ha a value a self értékei között szerepel, beleértve a végpontokat is, ha
        az intervallum azon az oldalon zárt.
        """
        return ((self._eq(self.lower_endpoint, value) * self.flags[0] or self.lower_endpoint < value) and
                (self._eq(self.upper_endpoint, value) * self.flags[1] or self.upper_endpoint > value))

    def __iter__(self) -> Iterator:
        """Olyan iterátort ad vissza, amely sorban kiadja az alsó és a felső végpontotokat, majd az ezekhez tartozó flagek értékeit."""
        return chain((self.lower_endpoint, self.upper_endpoint), self.flags)

    def length(self) -> int | float:
        """Visszaadja a végpontok közötti különbséget, azaz az intervallum hosszát, nemnegatív számként."""
        return self.upper_endpoint - self.lower_endpoint

    def midpoint(self) -> float:
        """Az intervallum középértékét adja vissza."""
        return (self.lower_endpoint + self.upper_endpoint) / 2

    def reprval(self, key: Literal['lower', 'upper', 'mid'] = 'lower') -> int | float:
        """Visszaadja az alsó és felső végpont, valamint középpont közül a key argumentummal
        kiválasztott értéket, amely az intervallumot fogja képviselni.
        """
        repr_values = {'lower': self.lower_endpoint, 'upper': self.upper_endpoint, 'mid': self.midpoint()}
        return repr_values[key]

    def split(self, n: int) -> Iterator[Interval]:
        """Az intervallumot n részintervallumra osztja.
        Ahhoz, hogy egy keresett érték csak egyetlen részintervallumban legyen megtalálható, minden részintervallum
        alsó végpontja megegyezik a felosztott intervallum alsó végpontjával, a felső végpontok
        ehhez igazodnak, hogy a csatlakozó végpontok zártsága/nyitottsága ellentétes legyen. Az utolsó részintervallum
        felső végpontja a felosztott intervallum felső végpontjának megfelelő lesz.
        """
        width = self.length() / n
        # Az első (n-1) darab részintervallum előállítása.
        iterable1 = (Interval.from_endpoint_values_and_flags(a, b, self.flags[0], self.flags[0] ^ 1)
                     for a, b in pairwise(self.lower_endpoint + width * i for i in range(n)))
        # Az utolsó részintervallum előállítása.
        iterable2 = [Interval.from_endpoint_values_and_flags(left_point := self.lower_endpoint + width * (n - 1), left_point + width,
                                                             self.flags[0], self.flags[1])]
        return chain(iterable1, iterable2)

    def sort(self, *others: Interval) -> list[Interval]:
        """Egy listával tér vissza, amelynek a self és az others argumentummal megadott intervallumok az elemei az
        alsó végpontjaik szerint növekvő sorrendben.
        """
        return sorted((self, *others), key=lambda _iv: _iv.lower_endpoint)

    def __and__(self, other: Interval) -> Interval | None:
        """Olyan új Interval példánnyal tér vissza, amely a self és other közös részét (metszetét) képviseli.
        Két intervallum közös része egy olyan intervallum, amelyben legalább egy olyan érték van, amely közös a két intervallumban.
        """
        _iv1, _iv2 = self.sort(other)

        if t := _iv1.adj_iv_common_endpoint(_iv2):
            _, flag1, flag2 = t
            if flag1 & flag2:
                return Interval.from_endpoints(_iv1.endpoints, _iv2.endpoints)
            else:
                return None

        elif not (_iv2 > _iv1):
            intersect_lower_value = _iv2.lower_endpoint
            if self._eq(_iv1.lower_endpoint, _iv2.lower_endpoint):
                intersect_lower_flag = _iv2.endpoints.lower.flag & _iv1.endpoints.lower.flag
            else:
                intersect_lower_flag = _iv2.endpoints.lower.flag
            intersect_upper_endpoint: IntervalEndpoint = min((_iv1.endpoints.upper, _iv2.endpoints.upper), key=lambda ep: ep.value)
            if self._eq(_iv1.upper_endpoint, _iv2.upper_endpoint):
                intersect_upper_flag = _iv2.endpoints.upper.flag & _iv1.endpoints.upper.flag
            else:
                intersect_upper_flag = intersect_upper_endpoint.flag
            return Interval.from_endpoint_values_and_flags(intersect_lower_value, intersect_upper_endpoint.value,
                                                           intersect_lower_flag, intersect_upper_flag)
        return None

    def __or__(self, other: Interval) -> Interval | None:
        """Olyan új Interval példánnyal tér vissza, amely a self és other egyesítésével jön létre.
        Az egyesített intervallumban minden érték szerepel, amely legalább az egyik összetevőnek eleme.
        Ha ez a feltétel nem teljesül, akkor a self és other nem egyesíthető egyetlen intervallummá.
        Ekkor a visszatérési érték None.
        """
        _iv1, _iv2 = self.sort(other)

        if t := _iv1.adj_iv_common_endpoint(_iv2):
            _, flag1, flag2 = t
            if flag1 | flag2:
                return Interval.from_endpoints(_iv1.endpoints, _iv2.endpoints)
            else:
                return None

        elif not (_iv2 > _iv1):
            union_lower_value = _iv1.lower_endpoint
            if self._eq(_iv1.lower_endpoint, _iv2.lower_endpoint):
                union_lower_flag = _iv1.endpoints.lower.flag | _iv2.endpoints.lower.flag
            else:
                union_lower_flag = _iv1.endpoints.lower.flag

            union_upper_endpoint: IntervalEndpoint = max((_iv1.endpoints.upper, _iv2.endpoints.upper), key=lambda ep: ep.value)
            if self._eq(_iv1.upper_endpoint, _iv2.upper_endpoint):
                union_upper_flag = _iv1.endpoints.upper.flag | _iv2.endpoints.upper.flag
            else:
                union_upper_flag = union_upper_endpoint.flag

            return Interval.from_endpoint_values_and_flags(union_lower_value, union_upper_endpoint.value,
                                                           union_lower_flag, union_upper_flag)
        return None

    def __add__(self, value: int | float) -> Interval:
        """Olyan új Interval példánnyal tér vissza, amely a végein ugyanúgy zárt/nyitott, mint self, de
        két végpontja a self végpontjaihoz képest value értékkel növeltek. Más szóval, az új intervallum
        a self-hez képest value értékkel el van tolva.
        """
        return type(self)(self.lower_endpoint + value, self.upper_endpoint + value, self.type)

    def __radd__(self, value: int | float) -> Interval:
        return self + value

    def __mul__(self, value: int | float) -> Interval:
        """Olyan új Interval példánnyal tér vissza, amely a végein ugyanúgy zárt/nyitott, mint self és középpontja
        megegyezik a self középpontjával, de szélessége value-szerese a self szélességének, ahol value > 0 valós szám.
        """
        if value <= 0:
            raise ValueError('Az argumentum pozítv valós szám kell, hogy legyen.')
        return type(self)(self.midpoint() - (self.midpoint() - self.lower_endpoint) * value,
                          self.midpoint() + (self.upper_endpoint - self.midpoint()) * value, self.type)

    def __rmul__(self, value: int | float) -> Interval:
        return self * value

    def adj_iv_common_endpoint(self, other: Interval) -> tuple:
        """Ha két intervallum szomszédos, akkor egy tuple-ban visszaadja a közös végpont értékét, valamint
        e point zártságát jelző flag értékeket az alsó végpontok szerint sorbarendezett intervallumok sorrendjében.
        A visszatérési érték egy üres tuple, ha a két intervallum nem szomszédos.
        Pl.: Ha iv1 = Interval(2, 5, IntervalType.CLOSED), iv2 = Interval(-1, 2, IntervalType.RIGHT_OPEN), akkor
        iv1.common_endpoint_and_flags(iv2) == (2, 0, 1)
        """
        if self.is_adjacent_to(other):
            _iv1, _iv2 = self.sort(other)
            return _iv1.upper_endpoint, _iv1.endpoints.upper.flag, _iv2.endpoints.lower.flag
        return ()

    def union(self, other: Interval) -> Interval | None:
        """Olyan új Interval példánnyal tér vissza, amely a self és other egyesítésével jön létre.
        Hatásában megegyezik a | operátoréval.
        """
        return self | other

    def intersection(self, other: Interval) -> Interval | None:
        """Olyan új Interval példánnyal tér vissza, amely a self és other közös részét (metszetét) képviseli.
        Hatásában megegyezik a & operátoréval.
        """
        return self & other

    def overlaps(self, other: Interval) -> bool:
        """Igaz értéket ad vissza, ha a self és other átlapolódó intervallumok.
        Két intervallum átlapolódik, ha legalább egy közös értékük van.
        """
        return bool(self & other)

    def is_subinterval(self, other: Interval) -> bool:
        """A self akkor részintervalluma az other intervallumnak, ha minden értéke other-nek is értéke.
        Ezért az egyenlő intervallumok is egymás részintervallumai.
        """
        # A self nem részintervallum, ha az alábbiek közül bármelyik igaz.
        # Az azonos oldali végpontok egyenlőek, de other az adott végponton nyitott.
        cond1 = self._eq(self.lower_endpoint, other.lower_endpoint) and (self.flags[0] == 1 and other.flags[0] == 0)
        cond2 = self._eq(self.upper_endpoint, other.upper_endpoint) and (self.flags[1] == 1 and other.flags[1] == 0)
        # A self alsó (felső) végpontja kisebb (nagyobb), mint az other alsó (felső) végpontja.
        cond3 = self.lower_endpoint < other.lower_endpoint
        cond4 = self.upper_endpoint > other.upper_endpoint
        return not (cond1 or cond2 or cond3 or cond4)

    def is_adjacent_to(self, other: Interval) -> bool:
        """Két intervallumot szomszédosnak tekintünk, ha a hosszuk összege megegyezik a legkisebb és legnagyobb
        végpotok által alkotott intervallum hosszával.
        Ha ez teljesül, akkor True értékkel tér vissza függetlenül attól, hogy az egyenlő értékű végpontok
        zártsága milyen (mindkét végpont zárt, csak valamelyik, vagy egyik sem).
        """
        _iv1, _iv2 = self.sort(other)
        return self._eq(_iv1.length() + _iv2.length(), Interval(_iv1.lower_endpoint, _iv2.upper_endpoint).length())

    def is_closed(self) -> bool:
        """Igaz értékkel tér vissza, ha az intervallum mindkét végpontján zárt."""
        return self.type == IntervalType.CLOSED

    def is_left_open(self) -> bool:
        """Igaz értékkel tér vissza, ha az intervallum alsó végpontján nyitott, felső végpontján zárt."""
        return self.type == IntervalType.LEFT_OPEN

    def is_right_open(self) -> bool:
        """Igaz értékkel tér vissza, ha az intervallum alsó végpontján zárt, felső végpontján nyitott."""
        return self.type == IntervalType.RIGHT_OPEN

    def is_open(self) -> bool:
        """Igaz értékkel tér vissza, ha az intervallum mindkét végpontján nyitott."""
        return self.type == IntervalType.OPEN

    def is_half_open(self) -> bool:
        """Igaz értékkel tér vissza, ha az intervallum egyik végpontján nyitott, a másikon zárt."""
        return self.type in (IntervalType.RIGHT_OPEN, IntervalType.LEFT_OPEN)


    
