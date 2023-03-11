def triangle_area(_length, _height):
    return 1 / 2 * _length * _height


def read_non_negative_int(var_name):
    while True:
        try:
            value = int(input(f"Enter {var_name}: "))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter non-negative integer value")


length = read_non_negative_int("length")
height = read_non_negative_int("height")

print(f"Triangle area = {triangle_area(length, height)}")
