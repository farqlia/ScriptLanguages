# dynamika - typ moze sie zmieniac
# statyka - typ nie moze sie zmieniac
from enum import Enum

pie = ["chocolate", "sugar"]
print(type(pie))
pie = 3.14
print(type(pie))

# typowanie
# w pythonie jest silne
Color = Enum('Color', ['RED', 'GREEN'])
# To nie jest wspieranie o ile nie zaimplementujemy
# sami
# Czyli nie sa wykonywane automatyczne
# koercje
# jezyk jest dynamiczny, silny
# Color.RED + 1 == Color.GREEN
# typow sie nie zaznacza
# mechanizm typow (opcjonalny)

# adnotacja typami nie ma wplywu na
# runtime - nadal mozemy podstawic dowolne
# obiekty
def repeat(text: str, how_many: int = 2) -> str:
    return how_many * text

# mypy to narzędzie do statycznej kontroli typow
print(repeat.__annotations__)

from typing import List, Tuple

# To jest pewnego rodzaju typ generyczny
# Krotka będzie elementem mniej dynamicznym
# ... - wiecej typow
def list2tuple(dos: List[str]) -> Tuple[str, ...]:
    return tuple(dos)

from typing import List, Union

# jedno lub drugie
def length(data: List[Union[str, int]]) -> int:
    return len(data)

from typing import Optional


def get_first_string(strings: List[str]) -> Optional[str]:
    if strings:
        return strings[0]
    else:
        return None

from typing import Any
# None to brak wartosci zwracanej
def print_any_value(value: Any) -> None:
    print(value)


from typing import Callable
# Callable to cos wywolywalnego - nie funkcja do konca
def my_fun(x: int, y:int, callback: Callable[[int, int], int]) -> int:
    return callback(x, y)

# Wariantnosc
# jesli t2 <: t1 (t2 jest podtypem t1), to
# kowariancja oznacza, że G[t2] <: G[t1]
# kontrawariantnosc : oznacza, ze G[t1] <: G[t2]
# zbadac ten slajd z wykladu 12

from dataclasses import dataclass

# Do pisania class, ktore sluza do przechowywania
# danych
#
@dataclass
class Duck:
    name: str
    age: int
    color: str
    weight: float = 1.0

duck = Duck(name='Daffy', age=3, color='black', weight=2.5)
