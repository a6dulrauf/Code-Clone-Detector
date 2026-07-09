function main() {
  const numbers = [5, 3, 8, 1, 9];
  while (numbers.length > 1) {
    numbers.sort();
    const smallest = numbers.shift();
    numbers[0] = numbers[0] + smallest;
  }

  const data = { total: numbers[0] };
  try {
    console.log(data.missing.value);
  } catch (e) {
    console.log(data.total);
  }
}

main();
