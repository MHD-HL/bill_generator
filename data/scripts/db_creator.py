import sqlite3

conn = sqlite3.connect("data\data.db")
c = conn.cursor()

###create a table
# c.execute(
#     """
#           CREATE TABLE IF NOT EXISTS bills (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             customer_name TEXT NOT NULL,
#             date DATE NOT NULL,
#             total_amount REAL NOT NULL
#           )
#         """
# )

###insert data into the table
# c.execute(
#     """
#     INSERT INTO bills (id, customer_name, date, total_amount) VALUES
#         (1, "ahmad", "12/8/2025", 69.0),
#         (2, "aya", "12/8/2025", 210.0),
#         (3, "ayham", "12/8/2025", 91.0),
#         """
# )

conn.commit()
conn.close()