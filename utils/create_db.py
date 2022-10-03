import sqlite3, random, datetime
import names


con = sqlite3.connect("rental.db")

cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON")

con.commit()

cur.execute("""CREATE TABLE user(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    age INTEGER, 
    sex TEXT
    )""")

con.commit()

cur.execute("""CREATE TABLE vehicle(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    type TEXT, 
    status TEXT
    )""")
    
con.commit()

cur.execute("""CREATE TABLE manager(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    age INTEGER, 
    sex TEXT,
    admin INTEGER
    )""")
    
con.commit()

cur.execute("""CREATE TABLE history(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER NOT NULL, 
    vehicle_id INTEGER NOT NULL, 
    start_date TEXT, 
    end_date TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (id)
    ON DELETE CASCADE ON UPDATE CASCADE
    )""")
    
con.commit()

cur.execute("""CREATE TABLE management(
    manager_id INTEGER NOT NULL,
    history_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    PRIMARY KEY (manager_id, history_id),
    FOREIGN KEY (manager_id) REFERENCES manager (id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (history_id) REFERENCES history (id)
    ON DELETE CASCADE ON UPDATE CASCADE
    )""")
    
con.commit()

# random user generator
for _ in range(10000):
    if random.choice([True, False]):
        cur.execute("""INSERT INTO user(name, age, sex)
            VALUES(?, ?, ?)
            """, (names.get_full_name(gender='male'), random.randint(18, 60), "Male",))
    else:
        cur.execute("""INSERT INTO user(name, age, sex)
            VALUES(?, ?, ?)
            """, (names.get_full_name(gender='female'), random.randint(18, 60), "Female",))

con.commit()

# random vehicle generator  
for _ in range(10000):
    if random.randint(1, 10) < 5:
        cur.execute("""INSERT INTO vehicle(type, status)
            VALUES(?, ?)
            """, ("Car", "Available",))
    elif 500 <= random.randint(1, 10) < 9:
        cur.execute("""INSERT INTO vehicle(type, status)
            VALUES(?, ?)
            """, ("Scooter", "Available",))
    else:
        cur.execute("""INSERT INTO vehicle(type, status)
            VALUES(?, ?)
            """, ("Boat", "Available",))

con.commit()

# random manager generator
for _ in range(500):
    if random.choice([True, False]):
        cur.execute("""INSERT INTO manager(name, age, sex, admin)
            VALUES(?, ?, ?, ?)
            """, (names.get_full_name(gender='male'), random.randint(18, 60), "Male", random.randint(1,3),))
    else:
        cur.execute("""INSERT INTO manager(name, age, sex, admin)
            VALUES(?, ?, ?, ?)
            """, (names.get_full_name(gender='female'), random.randint(18, 60), "Female", random.randint(1,3),))

con.commit()

# random history generator
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 1)
days_between_dates = (end_date - start_date).days
random_number_of_days = random.randrange(days_between_dates)
random_start_date = start_date + datetime.timedelta(days=random_number_of_days)
random_end_date = random_start_date + datetime.timedelta(days=random.randint(1, 28))

for _ in range(100000):
    random_number_of_days = random.randrange(days_between_dates)
    random_start_date = start_date + datetime.timedelta(days=random_number_of_days)
    random_end_date = random_start_date + datetime.timedelta(days=random.randint(1, 28))
    cur.execute("""INSERT INTO history(user_id, vehicle_id, start_date, end_date)
        VALUES(?, ?, ?, ?)
        """, (random.randint(1, 10000), random.randint(1, 10000), random_start_date, random_end_date,))

con.commit()

# random management generator
for _ in range(50000):
    cur.execute("""INSERT OR IGNORE INTO management(manager_id, history_id, type)
    VALUES(?, ?, ?)
    """, (random.randint(1, 500), random.randint(1, 100000), random.choice(["Web", "Mobile", "Offline"])))

con.commit()
