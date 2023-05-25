from typing import Protocol, runtime_checkable

'''
Nominal vs structural subtyping: with nominal subtyping, a class B is a 
subtype of class A <=> B explicitly subclasses A. Structural subtyping  
is based on the equivalence of actual structure (OCaml). It is still different
from duck typing, since the latter one bases on the structure accessed at 
runtime
Protocols were added for static type analysis & explicit subtyping of
classes declared as protocols (otherwise, even if all methods are compatible,
the class is not considered a subtype)
It is possible to subclass a Protocol, but it is not necessary to
'''

# Add this annotation since Protocols can't be instantiated directly
# and it needs a decorator to work with runtime checks
@runtime_checkable
class Duck(Protocol):

    def quack(self) -> None:
        ...

    def walk(self) -> None:
        ...


class RealDuck:

    def quack(self) -> None:
        print("quack")

    def walk(self) -> None:
        print("<walking>")


def kill(duck: Duck) -> None:
    for _ in range(2):
        duck.quack()


if __name__ == "__main__":

    real_duck = RealDuck()
    kill(real_duck)
    print(isinstance(real_duck, Duck))