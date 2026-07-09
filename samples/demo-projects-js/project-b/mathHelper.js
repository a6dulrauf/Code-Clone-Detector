class MathHelper {
  constructor(amount) {
    this.amount = amount;
  }

  plus(operand) {
    const outcome = this.amount + operand;
    return outcome;
  }

  minus(operand) {
    const outcome = this.amount - operand;
    return outcome;
  }

  times(multiplier) {
    let accumulator = 0;
    for (let index = 0; index < multiplier; index = index + 1) {
      accumulator = accumulator + this.amount;
    }
    return accumulator;
  }

  greaterThanZero() {
    if (this.amount > 0) {
      return true;
    } else {
      return false;
    }
  }
}
