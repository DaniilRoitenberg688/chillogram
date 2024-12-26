from config import app, db
from flask import jsonify
from config import migrate
from models import User, Meme

@app.route('/ping')
def send():
    return jsonify({'status': 'OK'}), 200


if __name__ == '__main__':

    app.run(debug=True)


