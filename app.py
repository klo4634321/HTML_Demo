from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)



@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        context = request.form['context']

        conn = sqlite3.connect('Devdb.db')  # ← 改成你自己的資料庫名稱
        c = conn.cursor()
        c.execute('INSERT INTO comment (name, context) VALUES (?, ?)', (name, context))
        conn.commit()
        conn.close()

        return redirect('/contact')  # 留言後重新整理頁面顯示新留言

    conn = sqlite3.connect('Devdb.db')
    c = conn.cursor()
    c.execute('SELECT name, context FROM comment ORDER BY id DESC')
    messages = c.fetchall()
    conn.close()

    return render_template('contact.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
