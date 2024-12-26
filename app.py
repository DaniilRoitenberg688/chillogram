from config import app, db
from flask import jsonify, render_template, session, request, redirect
from config import migrate
from models import User, Meme

@app.route('/ping')
def send():
    return jsonify({'status': 'OK'}), 200

@app.route('/')
def index():
    id = session.get('id', False)
    if id:
        user: User = User.query.filter_by(id=id).first()
        print(user.to_dict())
        return render_template('index.html', user=user.to_dict()['login'])

    return render_template('index.html')


@app.route('/auth/register_form')
def register_form():
    return render_template('register.html',
                           tilte='Регистрация')

@app.route('/auth/register', methods=['post', 'get'])
def register():
    user_login: str = request.form.get('login', -1)
    if user_login == -1:
        return render_template('register.html', message='No login',
                               tilte='Регистрация', login=user_login)

    if User.query.filter_by(login=user_login).first():
        return render_template('register.html', message='Not uniq login',
                               tilte='Регистрация', login=user_login)

    password = request.form.get('password', -1)
    password_again = request.form.get('password_again', -1)

    if password_again == -1 or password == -1:
        return render_template('register.html', message='No password',
                               tilte='Регистрация', login=user_login)

    if password_again != password:

        return render_template('register.html', message='Passwords do not match',
                               tilte='Регистрация', login=user_login)

    new_user = User(login=user_login)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/auth/login_form')


@app.route('/auth/login_form')
def login_form():
    return render_template('login.html',
                           tilte='login')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    user_login = request.form.get('login')
    user: User = User.query.filter_by(login=user_login).first()
    if not user:
        return render_template('login.html', title='login', message='No such user',
                               login=user_login)

    password = request.form.get('password')

    if not user.check_password(password):
        return render_template('login.html', title='login', message='Wrong password',
                               login=user_login)

    session['id'] = user.id
    return redirect('/')


@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':

    app.run(debug=True)


