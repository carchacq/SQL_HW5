import psycopg2

def create_db(conn):
    cur.execute("""
    DROP TABLE phone;
    DROP TABLE client;
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    email VARCHAR(40)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
    phone_id SERIAL PRIMARY KEY,
    phone_number VARCHAR,
    client_id INTEGER NOT NULL REFERENCES client(id)
    );
    """)
    conn.commit()

def add_client(conn, id, first_name, last_name, email):
    cur.execute("""
    INSERT INTO client VALUES(%s, %s, %s, %s);
    """, (id, first_name, last_name, email))
    conn.commit()


def add_phone(conn, phone_id, number, client_id):
    cur.execute("""
    INSERT INTO phone VALUES(%s, %s, %s);
    """, (phone_id, number, client_id))
    conn.commit()


def change_client(conn, id, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name:
        cur.execute("""
        UPDATE client SET first_name=%s WHERE id=%s;
        """, (first_name, id))

    if last_name:
        cur.execute("""
        UPDATE client SET last_name=%s WHERE id=%s;
        """, (last_name, id))

    if email:
        cur.execute("""
        UPDATE client SET email=%s WHERE id=%s;
        """, (email, id))

    if phone_number:
        cur.execute("""
        UPDATE phone SET phone_number=%s WHERE client_id=%s;
        """, (phone_number, id))


def delete_phone(conn, client_id, phone_number):
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s and phone_number=%s;
    """, (client_id, phone_number))


def delete_client(conn, client_id, id):
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s; 
    """, (client_id,))
    cur.execute("""
    DELETE FROM client WHERE id=%s;
    """, (id,))


def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name:
        cur.execute("""
        SELECT id, first_name, last_name, email, phone_number  FROM client c 
        LEFT JOIN phone p ON p.client_id = c.id
        WHERE first_name=%s;
        """, (first_name,))
        print(cur.fetchall())

    if last_name:
        cur.execute("""
        SELECT id, first_name, last_name, email, phone_number  FROM client c 
        LEFT JOIN phone p ON p.client_id = c.id
        WHERE last_name=%s;
        """, (last_name,))
        print(cur.fetchall())

    if email:
        cur.execute("""
        SELECT id, first_name, last_name, email, phone_number FROM client c 
        LEFT JOIN phone p ON p.client_id = c.id
        WHERE email=%s;
        """, (email,))
        print(cur.fetchall())

    if phone_number:
        cur.execute("""
        SELECT id, first_name, last_name, email, phone_number  FROM client c 
        LEFT JOIN phone p ON p.client_id = c.id
        WHERE phone_number=%s;
        """, (phone_number,))
        print(cur.fetchall())

with psycopg2.connect(database="clients_db", user="postgres", password="17991836") as conn:
    with conn.cursor() as cur:
        print(create_db(conn))
        print(add_client(conn, 1, 'Мирон', 'Фёдоров', 'oxxxymiron@gmail.com'))
        print(add_client(conn, 2, 'Алишер', 'Моргенштерн', email=None))
        print(add_phone(conn, 1, '89991234567', 1))
        print(add_phone(conn, 2, '89997654321', 1))
        print(add_phone(conn, 3, '89991234123', 2))
        print(change_client(conn, 2, 'Вася', 'Пупкин', 'pupkeen@mail.ru', '89006666666'))
        print(delete_phone(conn, 1, '89991234567'))
        print(delete_client(conn, 2, 2))
        print(find_client(conn, 'Мирон', last_name=None, email=None, phone_number=None))

conn.close()