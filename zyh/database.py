from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

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

# 处理查询请求的API
@app.route('/search', methods=['GET'])
def search_api():
    keyword = request.args.get('keyword')

    # 在数据库中根据关键字搜索匹配的结果
    results = search(keyword)

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')  # 处理跨域请求
    return response

# 处理保存选中结果的API
@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()

    # 将选中结果保存到文本文件并提供下载链接
    # ...

if __name__ == '__main__':
    app.run()
