from flask import Flask, request, render_template, redirect
import sqlite3
import os

app = Flask(__name__)


from flask import redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/projects')
def project():
    return render_template('projects.html')


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         context = request.form['context']

#         conn = sqlite3.connect('Devdb.db')  # ← 改成你自己的資料庫名稱
#         c = conn.cursor()
#         c.execute('INSERT INTO comment (name, context) VALUES (?, ?)', (name, context))
#         conn.commit()
#         conn.close()

#         return redirect('/contact')
    
#     conn = sqlite3.connect('Devdb.db')
#     c = conn.cursor()
#     c.execute('SELECT id, name, context FROM comment ORDER BY id DESC')
#     messages = c.fetchall()
#     conn.close()

#     return render_template('contact.html', messages=messages)

@app.route('/comment', methods=['POST'])
def comment():
    
    name = request.form['name']
    message = request.form['context']

    conn = sqlite3.connect('Devdb.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO comment (name, context) VALUES (?, ?)',
        (name, message)  # 留言功能不用 email，就空著
    )
    conn.commit()
    conn.close()
    return redirect('/contact')  # 留言完回到 contact 頁面

@app.route('/delete_comment', methods=['POST'])
def delete_comment():

    comment_id = request.form['id']
    print(f'收到要刪除的留言 ID：{comment_id}')  # 🔍 除錯用
    
    conn = sqlite3.connect('Devdb.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comment WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()
    return redirect('/contact')  # 刪除留言後回到 contact 頁面


def get_db_connection():
    conn = sqlite3.connect('Devdb.db')
    conn.row_factory = sqlite3.Row  # ★ 這一行很重要！
    return conn

@app.route('/contact')
def contact():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, context FROM comment')
    messages = cursor.fetchall()
    conn.close()
    return render_template('contact.html', messages=messages)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
