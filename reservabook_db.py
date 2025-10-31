import mysql.connector
from mysql.connector import Error

DB_NAME = "reservabook"

def _connect(database: str | None = DB_NAME):
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="KATYAL0786",
        database=database,
        autocommit=True,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        connection_timeout=30,
    )

def get_connection():
    try:
        return _connect(DB_NAME)
    except Error as e:
        if getattr(e, 'errno', None) == 1049 or 'Unknown database' in str(e):
            # Create database and retry
            root = _connect(None)
            cur = root.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cur.close()
            root.close()
            conn = _connect(DB_NAME)
            ensure_schema(conn)
            return conn
        raise

def ensure_schema(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INT PRIMARY KEY AUTO_INCREMENT,
            code VARCHAR(64) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            duration_min INT NOT NULL,
            price_cents INT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INT PRIMARY KEY AUTO_INCREMENT,
            service_code VARCHAR(64) NOT NULL,
            booking_date DATE NOT NULL,
            booking_time VARCHAR(16) NOT NULL,
            first_name VARCHAR(128) NOT NULL,
            last_name VARCHAR(128) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(32) NOT NULL,
            notes TEXT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_service_code FOREIGN KEY (service_code) REFERENCES services(code)
                ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    # Seed services if empty
    cur.execute("SELECT COUNT(*) FROM services")
    (count,) = cur.fetchone()
    if count == 0:
        cur.executemany(
            "INSERT INTO services (code, name, duration_min, price_cents) VALUES (%s, %s, %s, %s)",
            [
                ("consultation", "Consultation", 30, 5000),
                ("repair", "Repair Service", 60, 8500),
                ("installation", "Installation", 120, 12000),
                ("maintenance", "Maintenance", 45, 6500),
            ],
        )
    cur.close()


