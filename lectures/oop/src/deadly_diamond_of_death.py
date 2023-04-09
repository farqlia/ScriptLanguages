# Wywołania funkcji dziedziczonych
# działają jak BFS
class A:

    def met(self):
        print("A")


class B(A):

    def met(self):
        print("B")
        super().met()


class C(A):

    def met(self):
        print("C")
        super().met()


class D(B, C):

    def met(self):
        print("D")
        super().met()


if __name__ == "__main__":
    d = D()
    d.met()