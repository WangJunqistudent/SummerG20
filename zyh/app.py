from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# 在这里创建数据库连接
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')  # 数据库文件名为 database.db
        print('数据库连接成功')
    except sqlite3.Error as e:
        print(e)
    return conn

# 在这里创建数据库表
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

# 路由：获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        user = {
            'id': row[0],
            'name': row[1],
            'email': row[2]
        }
        users.append(user)
    return jsonify(users)

# 路由：创建新用户
@app.route('/users', methods=['POST'])
def create_user():
    conn = create_connection()
    cursor = conn.cursor()
    name = request.form.get('name')
    email = request.form.get('email')
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    return '用户创建成功'


if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    app.run()
