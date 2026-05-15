import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("budget_tracker.db")
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                CategoryName TEXT NOT NULL,
                Type TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT NOT NULL,
                Amount REAL NOT NULL,
                CategoryID INTEGER,
                FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subscriptions (
                SubscriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Amount REAL NOT NULL,
                DueDate INTEGER NOT NULL,
                CategoryID INTEGER,
                FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            )
        ''')
        self.conn.commit()

        self.cursor.execute("SELECT COUNT(*) FROM Categories")
        if self.cursor.fetchone()[0] == 0:
            defaults = [("Food", "Expense"), ("Transport", "Expense"), ("Salary", "Income")]
            self.cursor.executemany("INSERT INTO Categories (CategoryName, Type) VALUES (?, ?)", defaults)
            self.conn.commit()

    def get_categories(self):
        self.cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
        return self.cursor.fetchall()

    def add_transaction(self, date, amount, category_id):
        self.cursor.execute(
            "INSERT INTO Transactions (Date, Amount, CategoryID) VALUES (?, ?, ?)",
            (date, amount, category_id)
        )
        self.conn.commit()

    def get_transactions(self):
        self.cursor.execute("SELECT TransactionID, Date, Amount FROM Transactions")
        return self.cursor.fetchall()

    def get_transaction_by_id(self, transaction_id):
        self.cursor.execute("""
            SELECT Transactions.Date, Transactions.Amount, Categories.CategoryName
            FROM Transactions
            JOIN Categories ON Transactions.CategoryID = Categories.CategoryID
            WHERE TransactionID = ?
        """, (transaction_id,))
        return self.cursor.fetchone()

    def update_transaction(self, transaction_id, date, amount, category_id):
        self.cursor.execute(
            "UPDATE Transactions SET Date = ?, Amount = ?, CategoryID = ? WHERE TransactionID = ?",
            (date, amount, category_id, transaction_id)
        )
        self.conn.commit()

    def delete_transaction(self, transaction_id):
        self.cursor.execute("DELETE FROM Transactions WHERE TransactionID = ?", (transaction_id,))
        self.conn.commit()