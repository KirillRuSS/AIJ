import model as model
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/ready')
def http_ready():
    return 'OK'


@app.route('/take_exam', methods=['POST'])
def http_take_exam():
    request_data = request.get_json()
    tasks = request_data['tasks']
    answers = model.take_exam(tasks)
    return jsonify({
        'answers': answers
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
