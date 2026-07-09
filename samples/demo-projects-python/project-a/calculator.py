class Calculator:
    def __init__(self, value):
        self.value = value

    def add(self, number):
        result = self.value + number
        return result

    def subtract(self, number):
        result = self.value - number
        return result

    def multiply(self, factor):
        total = 0
        for i in range(factor):
            total = total + self.value
        return total

    def is_positive(self):
        if self.value > 0:
            return True
        else:
            return False
