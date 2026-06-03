# 🚀 SuperCache — Быстрое кэширование для Node.js

SuperCache — лёгкая библиотека для кэширования данных в памяти с поддержкой TTL, стратегий вытеснения и асинхронного API.

---

## 📦 Установка

```bash
npm install supercache
```

Или через yarn:

```bash
yarn add supercache
```

---

## ⚡ Быстрый старт

```js
const cache = require('supercache');

cache.set('user:42', { name: 'Алиса', age: 28 }, { ttl: 60 });
const user = cache.get('user:42');
console.log(user); // { name: 'Алиса', age: 28 }
```

---

## 🛠️ API

### `cache.set(key, value, options?)`

Записывает значение в кэш.

```js
cache.set('session:abc', { token: 'xyz' }, { ttl: 3600 });
```

| Параметр          | Тип       | По умолчанию | Описание                              |
|-------------------|-----------|--------------|---------------------------------------|
| `key`             | `string`  | —            | Уникальный ключ записи                |
| `value`           | `any`     | —            | Любое сериализуемое значение          |
| `options.ttl`     | `number`  | `Infinity`   | Время жизни в секундах                |
| `options.tags`    | `string[]`| `[]`         | Теги для групповой инвалидации        |
| `options.onEvict` | `function`| `undefined`  | Колбэк при вытеснении записи         |

---

### `cache.get(key)`

Возвращает значение или `undefined`, если запись истекла или не существует.

```js
const val = cache.get('session:abc'); // { token: 'xyz' } или undefined
```

---

### `cache.delete(key)`

Удаляет одну запись по ключу.

```js
cache.delete('session:abc');
```

---

### `cache.invalidateByTag(tag)`

Удаляет все записи, помеченные указанным тегом.

```js
cache.set('post:1', data, { tags: ['posts'] });
cache.set('post:2', data, { tags: ['posts'] });

cache.invalidateByTag('posts'); // удалит оба ключа
```

---

### `cache.wrap(key, fn, options?)`

Асинхронный хелпер: возвращает кэшированное значение или выполняет `fn` и сохраняет результат.

```js
const getUserFromDB = async (id) => {
  // тяжёлый запрос к базе данных
  return db.query('SELECT * FROM users WHERE id = ?', [id]);
};

// Первый вызов — идёт в базу, второй — из кэша
const user = await cache.wrap(
  `user:${id}`,
  () => getUserFromDB(id),
  { ttl: 300 }
);
```

---

## 📊 Стратегии вытеснения

SuperCache поддерживает несколько стратегий управления памятью:

| Стратегия | Ключ конфига | Описание                                              | Когда использовать              |
|-----------|-------------|--------------------------------------------------------|---------------------------------|
| LRU       | `'lru'`     | Вытесняет давно неиспользуемые записи                 | Общий случай                    |
| LFU       | `'lfu'`     | Вытесняет записи с наименьшей частотой обращений      | Горячие данные с разной частотой|
| FIFO      | `'fifo'`    | Вытесняет самые старые по времени добавления          | Простые очереди                 |
| TTL-only  | `'ttl'`     | Вытеснение только по истечении времени жизни          | Данные с предсказуемым сроком   |

Пример конфигурации:

```js
const cache = require('supercache').create({
  strategy: 'lru',
  maxSize: 500,       // максимум 500 записей
  maxMemoryMB: 128,   // не более 128 МБ
});
```

---

## 📈 Метрики

Получить статистику работы кэша можно через `cache.stats()`:

```js
const stats = cache.stats();
console.log(stats);
/*
{
  hits: 4821,
  misses: 193,
  hitRate: 0.9617,
  size: 312,
  memoryUsedMB: 14.7,
  evictions: 55
}
*/
```

| Поле            | Тип      | Описание                                  |
|-----------------|----------|-------------------------------------------|
| `hits`          | `number` | Количество успешных обращений к кэшу      |
| `misses`        | `number` | Количество промахов                       |
| `hitRate`       | `number` | Доля попаданий (от 0 до 1)                |
| `size`          | `number` | Текущее количество записей                |
| `memoryUsedMB`  | `number` | Занятая память в мегабайтах               |
| `evictions`     | `number` | Количество принудительно удалённых записей|

---

## 🧪 Тесты

```bash
npm test
```

Запуск с покрытием:

```bash
npm run test:coverage
```

Пример теста:

```js
describe('cache.wrap()', () => {
  it('должен кэшировать результат функции', async () => {
    let callCount = 0;
    const fn = async () => {
      callCount++;
      return 'данные';
    };

    const first  = await cache.wrap('k', fn, { ttl: 60 });
    const second = await cache.wrap('k', fn, { ttl: 60 });

    expect(first).toBe('данные');
    expect(second).toBe('данные');
    expect(callCount).toBe(1); // функция вызвана только один раз
  });
});
```

---

## 🗺️ Роадмап

| Версия  | Фича                                 | Статус        |
|---------|--------------------------------------|---------------|
| 1.0     | Базовое API: get / set / delete      | ✅ Готово      |
| 1.1     | TTL и автоматическое вытеснение      | ✅ Готово      |
| 1.2     | Стратегии LRU / LFU / FIFO           | ✅ Готово      |
| 1.3     | `cache.wrap()` + теги                | ✅ Готово      |
| 2.0     | Redis-адаптер                        | 🔄 В работе   |
| 2.1     | Кластерный режим                     | 📋 Планируется|
| 2.2     | Панель мониторинга (веб-интерфейс)   | 📋 Планируется|

---

## 📄 Лицензия

[MIT](./LICENSE) © 2026 SuperCache Contributors