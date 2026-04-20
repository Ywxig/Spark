# Лабораторная работа №2

## функция `forEach`

```JS

function forEach(array, callback) {
  if (!Array.isArray(array)) {
    throw new TypeError(array + ' is not an array');
  }

  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }

  for (let i = 0; i < array.length; i++) {
    callback(array[i], i, array);
  }
}

```
Функция *последовательно* перебирает элементы массива и выполняет для каждого из них заданное вами действие.

> возможные ощибки
> 1. Если передать вместо колбэка что-то другое (например, число или строку), возникнет ошибка.
> 2. Если вместо массива передать число или строку, функция также выдаст ошибку, так как ожидается именно массив.


## функция `map`

```JS
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
```

Функция создаёт новый массив, в который помещаются результаты вызова переданного вами действия для каждого элемента исходного массива.

> возможные ошибки
> 1. Если передать вместо колбэка что‑то другое (например, число или строку), возникнет ошибка.
> 2. Если вместо массива передать число или строку, функция также выдаст ошибку, так как ожидается именно массив.

## функция `filter`

```JS
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
```
Функция создаёт новый массив, в который помещаются те элементы исходного массива,
для которых переданное вами действие возвращает true (то есть отфильтрованные по
заданному условию).

> возможные ошибки
> 1. Если передать вместо колбэка что‑то другое (например, число или строку), возникнет ошибка.
> 2. Если вместо массива передать число или строку, функция также выдаст ошибку, так как ожидается именно массив.

## функция `find`

```JS
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
```

Функция последовательно перебирает элементы массива и возвращает первый элемент,
для которого переданное вами действие возвращает true. Если ни один элемент не
подошёл, возвращается undefined.

>возможные ошибки
> 1. Если передать вместо колбэка что‑то другое (например, число или строку), возникнет ошибка.
> 2. Если вместо массива передать число или строку, функция также выдаст ошибку, так как ожидается именно массив.

## функция `some`

```JS
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
```

Функция последовательно перебирает элементы массива и возвращает `true`,
если хотя бы для одного из них переданное вами действие возвращает `true`.
Если ни один элемент не подошёл, возвращается `false`.

> возможные ошибки
> 1. Если передать вместо колбэка что‑то другое (например, число или строку), возникнет ошибка.
> 2. Если вместо массива передать число или строку, функция также выдаст ошибку, так как ожидается именно массив.

## ответы на вопросы
Коротко и по делу:
1. В чем преимущества?

    - Читаемость: Ты пишешь, что хочешь сделать (отфильтровать, изменить), а не как перебирать индексы.

    - Иммутабельность: Методы возвращают новый массив, не ломая исходные данные.

    - Цепочки: Можно объединять действия в одну строку: arr.filter().map().

2. Проблемы и решения

    - Производительность: На массивах в миллионы элементов колбэки чуть медленнее цикла for.

        Решение: Использовать for, если важна каждая миллисекунда.

    - Потеря this: Обычные функции в колбэках теряют контекст объекта.

        Решение: Использовать стрелочные функции () => {}.

    - Ад колбэков: Вложенные друг в друга функции трудно читать.

        Решение: Разбивать код на именованные функции или использовать Promises/async-await.

3. Реализация без встроенных методов

      Map: let r = []; for(let i of a) r.push(cb(i)); return r; (создает измененную копию).

      Filter: let r = []; for(let i of a) if(cb(i)) r.push(i); return r; (отбирает по условию).

      Find: for(let i of a) if(cb(i)) return i; (возвращает первый совпавший или undefined).

      Some: for(let i of a) if(cb(i)) return true; return false; (хотя бы один подошел).

      Every: for(let i of a) if(!cb(i)) return false; return true; (все должны подойти).

      Reduce: let acc = init; for(let i of a) acc = cb(acc, i); return acc; (сжимает всё в одно значение).