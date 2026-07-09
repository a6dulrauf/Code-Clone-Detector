class Calculator {
  constructor(value) {
    this.value = value;
  }

  add(number) {
    const result = this.value + number;
    return result;
  }

  subtract(number) {
    const result = this.value - number;
    return result;
  }

  multiply(factor) {
    let total = 0;
    for (let i = 0; i < factor; i = i + 1) {
      total = total + this.value;
    }
    return total;
  }

  isPositive() {
    if (this.value > 0) {
      return true;
    } else {
      return false;
    }
  }
}
