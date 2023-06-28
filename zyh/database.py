import sqlite3

# 创建数据库连接
conn = sqlite3.connect('file_index.db')
cursor = conn.cursor()

# 建立索引的表结构
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        path TEXT,
        line_number INTEGER,
        content TEXT
    )
''')

# 插入数据
def insert_file(path, line_number, content):
    cursor.execute('''
        INSERT INTO files (path, line_number, content)
        VALUES (?, ?, ?)
    ''', (path, line_number, content))
    conn.commit()

# 查询匹配的结果
def search(keyword):
    cursor.execute('''
        SELECT path, line_number, content
        FROM files
        WHERE content LIKE ?
    ''', ('%' + keyword + '%',))
    results = cursor.fetchall()
    return results
