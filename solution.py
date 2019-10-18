from flask import Flask, request, jsonify

from CuttingEdgeStrongGeneralAI import CuttingEdgeStrongGeneralAI

app = Flask(__name__)

ai = CuttingEdgeStrongGeneralAI()


@app.route('/ready')
def http_ready():
    return 'OK'


@app.route('/take_exam', methods=['POST'])
def http_take_exam():
    request_data = request.get_json()
    answers = ai.take_exam(request_data)
    return jsonify({
        'answers': answers
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
