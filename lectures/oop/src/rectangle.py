import abc


class Figure(abc.ABC):

    @abc.abstractmethod
    def area(self):
        pass



class Rectangle(Figure):

    def area(self):
        # Call superclass version of the class
        super().area()


