from flask import Flask
from utils.connection import get_connection

app = Flask(__name__)


@app.route('/meteorite/get_data', methods=['GET'])
def _get_data():
    try:
        db = get_connection()
        res = list(db['meteorite'].find({}, {'_id': 0}))
        db.client.close()
        return {'content': res}, 200
    except Exception as e:
        print(e)
        return {'content': 'error'}, 500


if __name__ == '__main__':
    app.run()
