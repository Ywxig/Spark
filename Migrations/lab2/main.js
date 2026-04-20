function forEach(array, callback) {
  // 1. Проверяем, что первый аргумент — массив
  if (!Array.isArray(array)) {
    throw new TypeError(array + ' is not an array');
  }

  // 2. Проверяем, что второй аргумент — функция
  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }

  // 3. Используем обычный цикл for для обхода
  for (let i = 0; i < array.length; i++) {
    // 4. Вызываем колбэк со строгим набором аргументов:
    // элемент, индекс, сам массив
    callback(array[i], i, array);
  }

  // 5. Функция по умолчанию возвращает undefined
}

const fruits = ['apple', 'banana', 'cherry'];

forEach(fruits, (item, index) => {
  console.log(`Element ${index}: value ${item}`);
});

function map(array, callback) {
  if (!Array.isArray(array)) {
    throw new TypeError(array + ' is not an array');
  }

  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }

  const result = [];

  for (let i = 0; i < array.length; i++) {
    result.push(callback(array[i], i, array));
  }
  
  return result;
}

const numbers = [1, 2, 3];
const squares = map(numbers, (num) => num * num);
console.log(squares); // [1, 4, 9]

function filter(array, callback) {
  if (!Array.isArray(array)) {
    throw new TypeError(array + ' is not an array');
  }
  
  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }

    const result = [];

    for (let i = 0; i < array.length; i++) {
        if (callback(array[i], i, array)) {
            result.push(array[i]);
        }
    }

    return result;
}

const mixedNumbers = [1, -2, 3, -4, 5];
const positiveNumbers = filter(mixedNumbers, (num) => num > 0);
console.log(positiveNumbers); // [1, 3, 5]

function find(array, callback) {
  if (!Array.isArray(array)) {
    throw new TypeError(array + ' is not an array');
  }
    
    if (typeof callback !== 'function') {
        throw new TypeError(callback + ' is not a function');
    }

    for (let i = 0; i < array.length; i++) {
        if (callback(array[i], i, array)) {
            return array[i];
        }
    }

    return undefined;
}

const people = [
  { name: 'Carlos', number: 55 },
  { name: 'Charlie', number: 16 },
  { name: 'Max', number: 3 }
];

const person = find(people, (p) => p.number > 44);
console.log(person);

function some(array, callback) {
  if (!Array.isArray(array)) {
    throw new TypeError(array + ' is not an array');
  }
    
    if (typeof callback !== 'function') {
        throw new TypeError(callback + ' is not a function');
    }
    
    for (let i = 0; i < array.length; i++) {
        if (callback(array[i], i, array)) {
            return true;
        }
    }

    return false;
}

const hasNegative = some(mixedNumbers, (num) => num < 0);
console.log(hasNegative); // true

function every(array, callback) {
    if (!Array.isArray(array)) {
        throw new TypeError(array + ' is not an array');
    }

    if (typeof callback !== 'function') {
        throw new TypeError(callback + ' is not a function');
    }
    
    for (let i = 0; i < array.length; i++) {
        if (!callback(array[i], i, array)) {
            return false;
        }
    }

    return true;
}

const allPositive = every(mixedNumbers, (num) => num > 0);
console.log(allPositive); // false