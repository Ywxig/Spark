const transactions = [
  {
    transaction_id: "T001",
    transaction_date: "2024-01-15",
    transaction_amount: 250.00,
    transaction_type: "debit",
    transaction_description: "Grocery shopping",
    merchant_name: "SuperMart",
    card_type: "debit"
  },
  {
    transaction_id: "T002",
    transaction_date: "2024-01-22",
    transaction_amount: 1200.00,
    transaction_type: "credit",
    transaction_description: "Salary payment",
    merchant_name: "Employer Inc.",
    card_type: "credit"
  },
  {
    transaction_id: "T003",
    transaction_date: "2024-02-05",
    transaction_amount: 89.99,
    transaction_type: "debit",
    transaction_description: "Online subscription",
    merchant_name: "StreamService",
    card_type: "credit"
  },
  {
    transaction_id: "T004",
    transaction_date: "2024-02-14",
    transaction_amount: 350.00,
    transaction_type: "debit",
    transaction_description: "Restaurant dinner",
    merchant_name: "Fine Dining Co.",
    card_type: "debit"
  },
  {
    transaction_id: "T005",
    transaction_date: "2024-02-20",
    transaction_amount: 500.00,
    transaction_type: "credit",
    transaction_description: "Freelance payment",
    merchant_name: "ClientCorp",
    card_type: "debit"
  },
  {
    transaction_id: "T006",
    transaction_date: "2024-03-03",
    transaction_amount: 75.50,
    transaction_type: "debit",
    transaction_description: "Gas station",
    merchant_name: "FuelStop",
    card_type: "debit"
  },
  {
    transaction_id: "T007",
    transaction_date: "2024-03-10",
    transaction_amount: 430.00,
    transaction_type: "debit",
    transaction_description: "Electronics purchase",
    merchant_name: "TechStore",
    card_type: "credit"
  },
  {
    transaction_id: "T008",
    transaction_date: "2024-03-18",
    transaction_amount: 2000.00,
    transaction_type: "credit",
    transaction_description: "Bonus payment",
    merchant_name: "Employer Inc.",
    card_type: "credit"
  },
  {
    transaction_id: "T009",
    transaction_date: "2024-03-25",
    transaction_amount: 120.00,
    transaction_type: "debit",
    transaction_description: "Pharmacy",
    merchant_name: "HealthPlus",
    card_type: "debit"
  },
  {
    transaction_id: "T010",
    transaction_date: "2024-04-01",
    transaction_amount: 60.00,
    transaction_type: "debit",
    transaction_description: "Coffee and snacks",
    merchant_name: "CafeWorld",
    card_type: "debit"
  }
];

/**
 * Returns an array of unique transaction types.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {string[]} Unique transaction types.
 */
function getUniqueTransactionTypes(transactions) {
  return [...new Set(transactions.map(t => t.transaction_type))];
}

/**
 * Calculates the total sum of all transactions.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {number} Total amount.
 */
function calculateTotalAmount(transactions) {
  return transactions.reduce((sum, t) => sum + t.transaction_amount, 0);
}

/**
 * Calculates the total amount filtered by year, month and/or day.
 * All date parameters are optional.
 * @param {Object[]} transactions - Array of transactions.
 * @param {number} [year] - Four-digit year.
 * @param {number} [month] - Month number (1-12).
 * @param {number} [day] - Day of month (1-31).
 * @returns {number} Filtered total amount.
 */
function calculateTotalAmountByDate(transactions, year, month, day) {
  return calculateTotalAmount(transactions.filter(t => {
    const [y, m, d] = t.transaction_date.split("-").map(Number);
    return (!year || y === year) && (!month || m === month) && (!day || d === day);
  }));
}-

/**
 * Returns transactions of a given type.
 * @param {Object[]} transactions - Array of transactions.
 * @param {string} type - Transaction type ("debit" or "credit").
 * @returns {Object[]} Filtered transactions.
 */
function getTransactionByType(transactions, type) {
  return transactions.filter(t => t.transaction_type === type);
}

/**
 * Returns transactions within a date range (inclusive).
 * @param {Object[]} transactions - Array of transactions.
 * @param {string} startDate - Start date in "YYYY-MM-DD" format.
 * @param {string} endDate - End date in "YYYY-MM-DD" format.
 * @returns {Object[]} Filtered transactions.
 */
function getTransactionsInDateRange(transactions, startDate, endDate) {
  return transactions.filter(t => t.transaction_date >= startDate && t.transaction_date <= endDate);
}

/**
 * Returns transactions made with a specific merchant.
 * @param {Object[]} transactions - Array of transactions.
 * @param {string} merchantName - Name of the merchant.
 * @returns {Object[]} Filtered transactions.
 */
function getTransactionsByMerchant(transactions, merchantName) {
  return transactions.filter(t => t.merchant_name === merchantName);
}

/**
 * Calculates the average transaction amount.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {number} Average amount, or 0 if array is empty.
 */
function calculateAverageTransactionAmount(transactions) {
  return transactions.length === 0 ? 0 : calculateTotalAmount(transactions) / transactions.length;
}

/**
 * Returns transactions with amount in a given range (inclusive).
 * @param {Object[]} transactions - Array of transactions.
 * @param {number} min - Minimum amount.
 * @param {number} max - Maximum amount.
 * @returns {Object[]} Filtered transactions.
 */
function getTransactionsByAmountRange(transactions, min, max) {
  return transactions.filter(t => t.transaction_amount >= min && t.transaction_amount <= max);
}

/**
 * Calculates the total amount of debit transactions.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {number} Total debit amount.
 */
function calculateTotalDebitAmount(transactions) {
  return calculateTotalAmount(getTransactionByType(transactions, "debit"));
}

/**
 * Returns the month with the highest number of transactions.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {string|null} Month number as string, or null if array is empty.
 */
function findMostTransactionsMonth(transactions) {
  if (!transactions.length) return null;
  const counts = {};
  transactions.forEach(t => {
    const m = t.transaction_date.split("-")[1];
    counts[m] = (counts[m] || 0) + 1;
  });
  return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
}

/**
 * Returns the month with the most debit transactions.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {string|null} Month number as string, or null if no debit transactions.
 */
function findMostDebitTransactionMonth(transactions) {
  return findMostTransactionsMonth(getTransactionByType(transactions, "debit"));
}

/**
 * Determines which transaction type is more frequent.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {"debit"|"credit"|"equal"} Dominant type or "equal".
 */
function mostTransactionTypes(transactions) {
  const d = getTransactionByType(transactions, "debit").length;
  const c = getTransactionByType(transactions, "credit").length;
  return d > c ? "debit" : c > d ? "credit" : "equal";
}

/**
 * Returns transactions made before a given date.
 * @param {Object[]} transactions - Array of transactions.
 * @param {string} date - Cutoff date in "YYYY-MM-DD" format.
 * @returns {Object[]} Filtered transactions.
 */
function getTransactionsBeforeDate(transactions, date) {
  return transactions.filter(t => t.transaction_date < date);
}

/**
 * Finds a transaction by its unique ID.
 * @param {Object[]} transactions - Array of transactions.
 * @param {string} id - Transaction ID to search for.
 * @returns {Object|null} Matching transaction or null.
 */
function findTransactionById(transactions, id) {
  return transactions.find(t => t.transaction_id === id) || null;
}

/**
 * Returns an array of all transaction descriptions.
 * @param {Object[]} transactions - Array of transactions.
 * @returns {string[]} Array of descriptions.
 */
function mapTransactionDescriptions(transactions) {
  return transactions.map(t => t.transaction_description);
}

// Tests
console.log("1.", getUniqueTransactionTypes(transactions));
console.log("2.", calculateTotalAmount(transactions));
console.log("3.", calculateTotalAmountByDate(transactions, 2024, 3));
console.log("4.", getTransactionByType(transactions, "debit").map(t => t.transaction_id));
console.log("5.", getTransactionsInDateRange(transactions, "2024-02-01", "2024-02-28").map(t => t.transaction_id));
console.log("6.", getTransactionsByMerchant(transactions, "Employer Inc.").map(t => t.transaction_id));
console.log("7.", calculateAverageTransactionAmount(transactions).toFixed(2));
console.log("8.", getTransactionsByAmountRange(transactions, 100, 500).map(t => t.transaction_id));
console.log("9.", calculateTotalDebitAmount(transactions));
console.log("10.", findMostTransactionsMonth(transactions));
console.log("11.", findMostDebitTransactionMonth(transactions));
console.log("12.", mostTransactionTypes(transactions));
console.log("13.", getTransactionsBeforeDate(transactions, "2024-02-01").map(t => t.transaction_id));
console.log("14.", findTransactionById(transactions, "T005"));
console.log("15.", mapTransactionDescriptions(transactions));