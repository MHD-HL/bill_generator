import sqlite3

conn = sqlite3.connect("Data\sunway.db")
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS batteries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        capacity INT NOT NULL,
        working_system INT NOT NULL,
        type TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INT NOT NULL DEFAULT 0
    )
        """
)
c.execute(
    """
    CREATE TABLE IF NOT EXISTS inverters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        power REAL NOT NULL,
        type TEXT,
        price REAL NOT NULL,
        quantity INT NOT NULL DEFAULT 0
    )
        """
)
c.execute(
    """
    CREATE TABLE IF NOT EXISTS solar_panels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        wattage INT NOT NULL,
        type TEXT,
        price REAL NOT NULL,
        quantity INT NOT NULL DEFAULT 0
    )
        """
)

c.execute(
    """
          CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            date DATE NOT NULL,
            total_amount REAL NOT NULL
          )
        """
)

c.execute(
    """
    INSERT INTO batteries (name, capacity, working_system, type, price, quantity) VALUES 
        ('Suness Battery', 100, 12, 'Lithium', 100.0, 10),
        ('Suness Battery', 200, 12, 'Lithium', 200.0, 10),
        ('Suness Battery', 300, 12, 'Lithium', 300.0, 10),
        ('Suness Battery', 100, 24, 'Lithium', 200.0, 10),
        ('Suness Battery', 200, 24, 'Lithium', 400.0, 10),
        ('Suness Battery', 300, 24, 'Lithium', 800.0, 10),
        ('Suness Battery', 100, 48, 'Lithium', 400.0, 10),
        ('Suness Battery', 200, 48, 'Lithium', 800.0, 10),
        ('Suness Battery', 300, 48, 'Lithium', 1600.0, 10),          
        ('TuffBull', 240, 12, 'Lead-acid', 250.0, 10)
        """
)
c.execute(
    """
    INSERT INTO inverters (name, power, type, price, quantity) VALUES 
        ('Deye Inverter', 6000, '', 450.0, 10),
        ('Deye Inverter', 8000, '', 1000.0, 10),
        ('Deye Inverter', 12000, '', 1500.0, 10),
        ('Deye Inverter', 20000, '', 2200.0, 10),
        ('Deye Inverter', 50000, '', 4500.0, 10)
        """
)
c.execute(
    """
    INSERT INTO solar_panels (name, wattage, type, price, quantity) VALUES
        ('Longi Solar Panel', 595, '', 89.0, 10),
        ('Longi Solar Panel', 595, '', 89.0, 10),
        ('Jinko Solar Panel', 710, '', 91.0, 10),
        ('Jinko Solar Panel', 710, '', 91.0, 10)
        """
)

conn.commit()
conn.close()
