from utils.add import add

result = add(1, 2)
print(f"Result of addition: {result}")

def sum_of_values(value_1: int, value_2: int) -> int:
    """
    Функция, суммирующая два числа
    """
    summa = value_1 + value_2
    return summa


def sub_of_values(value_1, value_2):
    """
    Функция, вычитающая два числа
    """
    subtract = value_1 - value_2
    return subtract