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
        all_memes = Meme.query.all()
        all_memes = [meme.to_dict() for meme in all_memes]
        return render_template('index.html', user=user.to_dict()['login'], all_memes=all_memes)

    return render_template('index.html')

@app.route('/sorted')
def index_sorted():
    id = session.get('id', False)
    if id:
        user: User = User.query.filter_by(id=id).first()
        all_memes = Meme.query.all()
        all_memes = [meme.to_dict() for meme in all_memes]
        all_memes = sorted(all_memes, key=lambda x: -x['likes'])[:20]
        return render_template('index.html', user=user.to_dict()['login'], all_memes=all_memes)

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


@app.route('/profile')
def profile():
    id = session.get('id')
    user: User = User.query.filter_by(id=id).first()
    all_memes = Meme.query.filter_by(user_id=id).all()
    all_memes = [meme.to_dict() for meme in all_memes]
    return render_template('profile.html', all_memes=all_memes, user=user.login, profile=True)


@app.route('/add_meme_form')
def add_meme_form():
    user = session.get('id')
    user: User = User.query.filter_by(id=user).first()
    return render_template('add_meme.html', title='add meme', user=user.login)


@app.route('/add_meme', methods=['POST', 'GET'])
def add_meme():
    user_id = session.get('id')
    user: User = User.query.filter_by(id=user_id).first()

    name = request.form.get('name', False)
    text = request.form.get('text', False)
    image = request.form.get('image', False)


    if not name:
        return render_template('add_meme.html', title='Добавление заметки',
                               message='Укажите название заметки', text=text, name=name, image=image, user=user.login)

    if not text:
        return render_template('add_meme.html', title='Добавление заметки',
                               message='Укажите текст заметки', name=name, text=text, image=image, user=user.login)

    if not image:
        return render_template('add_meme.html', title='Добавление заметки',
                               message='Укажите текст заметки', name=name, text=text, image=image, user=user.login)


    new_meme = Meme(
        name=name,
        image=image,
        description=text,
        likes=0,
        user_id=user_id
    )

    db.session.add(new_meme)
    db.session.commit()

    return redirect('/profile')


@app.route('/add_like/<id>')
def add_like(id):
    meme = Meme.query.filter_by(id=id).first()
    meme.likes += 1
    db.session.commit()
    return redirect('/')

@app.route('/remove_like/<id>')
def remove_like(id):
    meme = Meme.query.filter_by(id=id).first()
    meme.likes -= 1
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
