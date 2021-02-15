import sqlite3
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/enter-new/')
def enter_new_student():
    return render_template('student.html')


@app.route('/add_new_record/', methods=['POST', 'GET'])
def add_new_record():
    if request.method == "POST":
        try:
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
                cur.execute("INSERT INTO students (name, addr, city, pin) VALUES (?, ?, ?, ?)", (name, addr, city, pin))
                con.commit()
                msg = "Record successfully added."

        except:
            con.rollback()
            msg = "Error occurred in insert operation: "

        finally:
            con.close()
            return render_template('result.html', msg=msg)
            con.close()


@app.route('/show-records/')
def show_records():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    record = cur.fetchall()
    return render_template("records.html", rows=record)


if __name__ == '__main__':
    app.run(debug=True)

