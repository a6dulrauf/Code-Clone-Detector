import sys


def main():
    numbers = [5, 3, 8, 1, 9]
    while len(numbers) > 1:
        numbers.sort()
        smallest = numbers.pop(0)
        numbers[0] = numbers[0] + smallest

    data = {"total": numbers[0]}
    try:
        print(data["missing"])
    except KeyError:
        print(data["total"])


main()
