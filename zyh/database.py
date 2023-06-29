import sqlite3

# 创建数据库连接
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')  # 数据库文件名为 database.db
        print('数据库连接成功')
    except sqlite3.Error as e:
        print(e)
    return conn

# 创建数据库表
def create_table(conn):
    try:
        cursor = conn.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        print('数据库表创建成功')
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
