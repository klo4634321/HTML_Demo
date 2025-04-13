from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)



# MySQL 設定
db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="ray",
    password="123",  # 請依你的帳號密碼填寫
    database="html",
    charset="utf8mb4"
)

# Flask 建立完 app 之後直接印一次
cursor = db.cursor()
cursor.execute("SELECT * FROM comments ORDER BY id DESC LIMIT 1")
latest_comment = cursor.fetchone()
print("伺服器啟動時的最新留言：", latest_comment)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("content")

        sql = "INSERT INTO comments (name, content) VALUES (%s, %s)"
        cursor.execute(sql, (name, content))
        db.commit()
        return redirect("/contact")

    # 從資料庫讀留言
    cursor.execute("SELECT name, content, created_at FROM comments ORDER BY created_at DESC")
    comments = cursor.fetchall()

    return render_template("contact.html", comments=comments)

if __name__ == "__main__":
    app.run(debug=True)
