from config import app, db
from flask import jsonify, render_template, session
from config import migrate
from models import User, Meme

@app.route('/ping')
def send():
    return jsonify({'status': 'OK'}), 200

@app.route('/')
def index():
    is_auth = session.get('id', False)
    return render_template('index.html', is_auth=is_auth)


@app.route('/auth/register', methods=['POST', 'GET'])
def register():
    pass

if __name__ == '__main__':

    app.run(debug=True)


