from flask import Flask, request
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


@app.route('/meteorite/add_data', methods=['POST'])
def _add_data():
    try:
        db = get_connection()
        data = request.json
        res = db['meteorite'].insert_many(data)
        db.client.close()
        return {'content': "Les données ont bien été ajoutées"}, 200
    except Exception as e:
        print(e)
        return {'content': 'error'}, 500


if __name__ == '__main__':
    app.run(debug=True)
