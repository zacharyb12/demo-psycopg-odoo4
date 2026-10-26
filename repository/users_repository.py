from psycopg import Connection


def get_all_users(conn:"Connection"):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

def get_user_by_id(conn : "Connection" , id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s",(id,))
        
        user = cursor.fetchone()
        
        return user

def create_user(conn : "Connection",email,lastname,role):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (email,last_name,role)
            VALUES (%s,%s,%s)
            RETURNING id
            """
            , (email,lastname,role)
        )
        user_id = cursor.fetchone()[0]
        return user_id


def update_user(conn : "Connection",email,lastname,id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE users 
            SET 
            email = %s,
            last_name = %s
            WHERE id = %s
            """
            ,(email,lastname,id)
        )
        count_rows = cursor.rowcount
        return count_rows

def delete_user(conn : "Connection" , id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s",(id,))
        count_rows = cursor.rowcount
        return count_rows