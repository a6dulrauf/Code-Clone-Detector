class MathHelper:
    def __init__(self, amount):
        self.amount = amount

    def plus(self, operand):
        outcome = self.amount + operand
        return outcome

    def minus(self, operand):
        outcome = self.amount - operand
        return outcome

    def times(self, multiplier):
        accumulator = 0
        for index in range(multiplier):
            accumulator = accumulator + self.amount
        return accumulator

    def greater_than_zero(self):
        if self.amount > 0:
            return True
        else:
            return False
