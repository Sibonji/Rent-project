from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_login import LoginManager
import hashlib

PYTHONHASHSEED=0

import sqlite3 as sq

app = Flask(__name__)
content = [
    {
        'title': 'Ozon Rent',
		  }
]

login_manager = LoginManager()

class User(UserMixin):
    id = 0
    username = "name"
    password_hash = "123"

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
  print(User.query.get(user_id))
  return User.query.get(user_id)

@app.route('/')
def index():
    connection = sq.connect('db/postamates.db')
    cursor = connection.cursor()
    
    request_db = '''
    SELECT postamate_loc, postamate_id, count (door_id) 
    FROM postamate INNER JOIN door USING (postamate_id)
    GROUP BY postamate_loc, postamate_id
    '''
    cursor.execute(request_db)
    posts = cursor.fetchall()

    cursor.close()
    connection.close()
    print(posts)
    return render_template('index.html', 
	posts=posts,
	title='Ozon Rent', 
    description='Решение для аренды вещей, способных облегчить бытовую жизнь.',
    cover='https://www.python.org/static/opengraph-icon-200x200.png'
	)

@app.route('/post/<int:post_id>')
def post(post_id):
    connection = sq.connect('db/postamates.db')
    cursor = connection.cursor()
    
    request_db = '''
    SELECT door_id, item_status, item_name, item_link, item_img, postamate_id 
    FROM door 
    WHERE postamate_id = (?)
    '''
    cursor.execute(request_db, [post_id])
    posts = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('post.html', 
	posts=posts
	)

@app.route('/rent/<int:post_id>/<int:door_id>', methods=['GET', 'POST'])
def door(post_id, door_id):
    connection = sq.connect('db/postamates.db')
    cursor = connection.cursor()
    
    request_db = '''
    SELECT door_id, item_status, item_name, item_link, item_img, postamate_id 
    FROM door 
    WHERE postamate_id = (?) AND door_id = (?)
    '''
    cursor.execute(request_db, [post_id, door_id])
    post = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('rent.html', 
    post=post[0],
    err = 0
    )
    
@app.route('/rent_res/<int:post_id>/<int:door_id>', methods=['GET', 'POST'])
def door_res(post_id, door_id):
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']

        connection = sq.connect('db/postamates.db')
        cursor = connection.cursor()
        
        request_db = '''
        SELECT door_id, item_status, item_name, item_link, item_img, postamate_id 
        FROM door 
        WHERE postamate_id = (?) AND door_id = (?)
        '''
        cursor.execute(request_db, [post_id, door_id])
        post = cursor.fetchall()

        cursor.close()
        connection.close()

        connection = sq.connect('db/users.db')
        cursor = connection.cursor()
        
        hash_obj = hashlib.sha256(password.encode('ascii'))
        pwd_hash = hash_obj.hexdigest()

        request_db = '''
        SELECT nickname, user_pwd_hash, user_id
        FROM user
        WHERE nickname = (?) AND user_pwd_hash = (?)
        '''
        cursor.execute(request_db, [username, pwd_hash])
        res = cursor.fetchall()

        cursor.close()
        connection.close()

        if not res:
            return render_template('rent.html', 
            post=post[0],
            err = 1
            )
        else:
            connection = sq.connect('db/postamates.db')
            cursor = connection.cursor()
            now = datetime.datetime.now()
            now.strftime('%Y-%m-%d %H:%M:%S')

            request_db = '''
            UPDATE door
            SET item_status = 0, user_id = (?), taken_time = (?)
            WHERE postamate_id = (?) AND door_id = (?)
            '''
            cursor.execute(request_db, [res[0][2], now, post_id, door_id])
            connection.commit()

            cursor.close()
            connection.close()

    return render_template('success.html')
    # Тут будет подключение к серверу и открытие двери

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/log_res', methods=['GET', 'POST'])
def login_res():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']

        connection = sq.connect('db/users.db')
        cursor = connection.cursor()
        
        hash_obj = hashlib.sha256(password.encode('ascii'))
        pwd_hash = hash_obj.hexdigest()
        print(pwd_hash, username, password)

        request_db = '''
        SELECT nickname, user_pwd_hash, user_id, phone_number
        FROM user
        WHERE nickname = (?) AND user_pwd_hash = (?)
        '''
        cursor.execute(request_db, [username, pwd_hash])
        res = cursor.fetchall()
        print(res)

        cursor.close()
        connection.close()

        if not res:
            return render_template('login.html',
            err = 1
            )
        return render_template('profile.html', name=username, number=res[0][3])

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/reg_res', methods=['GET', 'POST'])
def registration_res():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        phone_number = request.form['phone']
        
        if not username or not password or not phone_number:
            return render_template('registration.html',
            err = 1
            )

        connection = sq.connect('db/users.db')
        cursor = connection.cursor()
        
        hash_obj = hashlib.sha256(password.encode('ascii'))
        pwd_hash = hash_obj.hexdigest()
        print(password, pwd_hash)

        request_db = '''
        INSERT INTO user (nickname, user_pwd_hash, phone_number) VALUES (?, ?, ?)
        '''
        cursor.execute(request_db, [username, pwd_hash, phone_number])
        connection.commit()

        cursor.close()
        connection.close()

        return render_template('profile.html', name=username, number=phone_number)
	
if __name__ == '__main__':
    app.run(debug=True)