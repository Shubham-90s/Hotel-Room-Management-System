# app.py

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hotel_management"
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number INT NOT NULL,
    capacity INT NOT NULL,
    status VARCHAR(20) NOT NULL
)
""")
db.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    return render_template('index.html', rooms=rooms)

@app.route('/add', methods=['POST'])
def add_room():
    room_number = request.form['room_number']
    capacity = request.form['capacity']
    status = request.form['status']
    cursor.execute("INSERT INTO rooms (room_number, capacity, status) VALUES (%s, %s, %s)", (room_number, capacity, status))
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_room(id):
    cursor.execute("SELECT * FROM rooms WHERE id = %s", (id,))
    room = cursor.fetchone()
    return render_template('edit.html', room=room)

@app.route('/update/<int:id>', methods=['POST'])
def update_room(id):
    room_number = request.form['room_number']
    capacity = request.form['capacity']
    status = request.form['status']
    cursor.execute("UPDATE rooms SET room_number = %s, capacity = %s, status = %s WHERE id = %s", (room_number, capacity, status, id))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_room(id):
    cursor.execute("DELETE FROM rooms WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
