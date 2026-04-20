/**
 * @fileoverview Лабораторная работа: Система инвентаря
 * Демонстрация классов, наследования, функций-конструкторов и опциональной цепочки в JavaScript.
 */


// ШАГ 1 — Класс Item (через синтаксис class)


/**
 * Представляет предмет в инвентаре.
 */
class Item {
  /**
   * @param {string} name    - Название предмета.
   * @param {number} weight  - Вес предмета (кг).
   * @param {string} rarity  - Редкость: 'common' | 'uncommon' | 'rare' | 'legendary'.
   */
  constructor(name, weight, rarity) {
    this.name = name;
    this.weight = weight;
    this.rarity = rarity;
  }

  /**
   * Возвращает строку с информацией о предмете.
   * @returns {string} Описание предмета.
   */
  getInfo() {
    return `[${this.rarity.toUpperCase()}] ${this.name} | Вес: ${this.weight} кг`;
  }

  /**
   * Изменяет вес предмета.
   * @param {number} newWeight - Новый вес (кг). Должен быть > 0.
   */
  setWeight(newWeight) {
    if (newWeight <= 0) {
      console.warn(`setWeight: вес должен быть больше 0 (получено ${newWeight})`);
      return;
    }
    this.weight = newWeight;
    console.log(`Вес "${this.name}" обновлён до ${this.weight} кг`);
  }
}


// ШАГ 2 — Класс Weapon, расширяющий Item
/**
 * Утилита для зажатия значения в заданном диапазоне [min, max].
 * @param {number} value - Значение для зажатия.
 * @param {number} min   - Минимальное значение.
 * @param {number} max   - Максимальное значение.
 * @returns {number} Зажатое значение.
 */
function clamp(value, min, max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

/**
 * Представляет оружие — расширение класса Item.
 * @extends Item
 */
class Weapon extends Item {
  /**
   * @param {string} name       - Название оружия.
   * @param {number} weight     - Вес оружия (кг).
   * @param {string} rarity     - Редкость.
   * @param {number} damage     - Урон оружия.
   * @param {number} durability - Прочность (0–100).
   */
  constructor(name, weight, rarity, damage, durability) {
    super(name, weight, rarity);      // вызов конструктора родителя
    this.damage = damage;
    this.durability = clamp(durability, 0, 100); // гарантируем, что прочность в пределах 0–100
  }

  /**
   * Возвращает расширенную информацию об оружии.
   * @returns {string} Описание оружия с уроном и прочностью.
   */
  getInfo() {
    return `${super.getInfo()} | Урон: ${this.damage} | Прочность: ${this.durability}/100`;
  }

  /**
   * Использует оружие: уменьшает прочность на 10.
   * Если прочность уже равна 0 — оружие нельзя использовать.
   */
  use() {
    if (this.durability <= 0) {
      console.log(`"${this.name}" сломано и не может быть использовано!`);
      return;
    }
    this.durability = Math.max(0, this.durability - 10);
    console.log(`"${this.name}" использовано. Прочность: ${this.durability}/100`);
  }

  /**
   * Ремонтирует оружие, восстанавливая прочность до 100.
   */
  repair() {
    this.durability = 100;
    console.log(`"${this.name}" отремонтировано. Прочность: ${this.durability}/100`);
  }
}


// ШАГ 3 — Тестирование классов


console.log("=== ШАГ 3: Тестирование классов ===\n");

const sword = new Item("Steel Sword", 3.5, "rare");
console.log(sword.getInfo());
sword.setWeight(4.0);
console.log(sword.getInfo() + "\n");

const muramassa = new Item("Muramassa", 5.0, "legendary");
console.log(muramassa.getInfo());
muramassa.setWeight(6.0);
console.log(muramassa.getInfo() + "\n");

const bow = new Weapon("Longbow", 2.0, "uncommon", 15, 100);
console.log(bow.getInfo());
bow.use();
bow.use();
console.log("Прочность лука:", bow.durability); // 80
bow.repair();
console.log("После ремонта:", bow.durability + "\n");  // 100

const legendaryAxe = new Weapon("Axe of Doom", 7.5, "legendary", 80, 100);
console.log(legendaryAxe.getInfo());
// Использовать 10 раз, чтобы сломать
for (let i = 0; i < 11; i++) legendaryAxe.use();


// ШАГ 4А — Опциональная цепочка (?.)
/*
данный механизм позволяет безопасно обращаться к свойствам и методам объектов, которые могут
быть null или undefined, предотвращая возникновение ошибок типа TypeError. В нашем случае мы можем использовать
опциональную цепочку при попытке получить информацию о предмете, который может отсутствовать в инвентаре.
*/

console.log("\n=== ШАГ 4А: Опциональная цепочка (?.) ===\n");

/**
 * Безопасно возвращает информацию о предмете с помощью опциональной цепочки.
 * Позволяет избежать TypeError, если item равен null или undefined.
 * @param {Item|null|undefined} item - Предмет инвентаря или отсутствующее значение.
 * @returns {string} Информация о предмете или сообщение об отсутствии.
 */
function printItemInfo(item) {
  // ?. не вызовет ошибку, если item === null/undefined
  const info = item?.getInfo() ?? "Предмет не найден";
  console.log(info);
}

printItemInfo(sword); // выведет информацию
printItemInfo(null); // "Предмет не найден"
printItemInfo(undefined); // "Предмет не найден"

// Опциональная цепочка при доступе к вложенным свойствам
const items = [sword, bow, null, legendaryAxe];
items.forEach((item, i) => {
  const name = item?.name ?? "(пусто)";
  console.log(`Слот ${i + 1}: ${name}`);
});


// ШАГ 4Б — Функции-конструкторы (аналог классов)


console.log("\n=== ШАГ 4Б: Функции-конструкторы ===\n");

/**
 * Функция-конструктор для предмета инвентаря.
 * Аналог класса Item, реализованный через старый синтаксис ES5.
 *
 * @constructor
 * @param {string} name - Название предмета.
 * @param {number} weight - Вес предмета (кг).
 * @param {string} rarity - Редкость предмета.
 */
function ItemConstructor(name, weight, rarity) {
  this.name   = name;
  this.weight = weight;
  this.rarity = rarity;
}

/**
 * Возвращает строку с информацией о предмете.
 * Определяется на прототипе, чтобы метод был общим для всех экземпляров.
 * @returns {string} Описание предмета.
 */
ItemConstructor.prototype.getInfo = function () {
  return `[${this.rarity.toUpperCase()}] ${this.name} | Вес: ${this.weight} кг`;
};

/**
 * Изменяет вес предмета.
 * @param {number} newWeight - Новый вес (кг).
 */
ItemConstructor.prototype.setWeight = function (newWeight) {
  if (newWeight <= 0) {
    console.warn(`setWeight: вес должен быть больше 0`);
    return;
  }
  this.weight = newWeight;
  console.log(`Вес "${this.name}" обновлён до ${this.weight} кг`);
};

// ---

/**
 * Функция-конструктор для оружия.
 * Наследует от ItemConstructor через Object.create.
 *
 * @constructor
 * @param {string} name       - Название оружия.
 * @param {number} weight     - Вес (кг).
 * @param {string} rarity     - Редкость.
 * @param {number} damage     - Урон.
 * @param {number} durability - Прочность (0–100).
 */
function WeaponConstructor(name, weight, rarity, damage, durability) {
  // Вызываем конструктор родителя в контексте текущего объекта
  ItemConstructor.call(this, name, weight, rarity);
  this.damage = damage;
  this.durability = clamp(durability, 0, 100); // гарантируем, что прочность в пределах 0–100
}

// Настраиваем цепочку прототипов: WeaponConstructor → ItemConstructor
WeaponConstructor.prototype = Object.create(ItemConstructor.prototype);
WeaponConstructor.prototype.constructor = WeaponConstructor;

/**
 * Переопределяет getInfo для оружия.
 * @returns {string} Полное описание оружия.
 */
WeaponConstructor.prototype.getInfo = function () {
  // Вызываем метод родителя через прототип
  const base = ItemConstructor.prototype.getInfo.call(this);
  return `${base} | Урон: ${this.damage} | Прочность: ${this.durability}/100`;
};

/**
 * Использует оружие: уменьшает прочность на 10.
 */
WeaponConstructor.prototype.use = function () {
  if (this.durability <= 0) {
    console.log(`"${this.name}" сломано!`);
    return;
  }
  this.durability = Math.max(0, this.durability - 10);
  console.log(`"${this.name}" использовано. Прочность: ${this.durability}/100`);
};

/**
 * Ремонтирует оружие.
 */
WeaponConstructor.prototype.repair = function () {
  this.durability = 100;
  console.log(`"${this.name}" отремонтировано. Прочность: ${this.durability}/100`);
};

// --- Тестирование функций-конструкторов ---

const shield  = new ItemConstructor("Iron Shield", 5.0, "common");
console.log(shield.getInfo());
shield.setWeight(5.5);

const dagger = new WeaponConstructor("Shadow Dagger", 0.8, "rare", 25, 100);
console.log(dagger.getInfo());
dagger.use();
dagger.use();
console.log("Прочность кинжала:", dagger.durability); // 80

// Проверка цепочки прототипов
console.log("\nПроверка instanceof:");
console.log("dagger instanceof WeaponConstructor:", dagger instanceof WeaponConstructor); // true
console.log("dagger instanceof ItemConstructor:",   dagger instanceof ItemConstructor); // true
console.log("sword instanceof Item:",               sword instanceof Item); // true
console.log("bow instanceof Item:",                 bow instanceof Item); // true
console.log("bow instanceof Weapon:",               bow instanceof Weapon); // true