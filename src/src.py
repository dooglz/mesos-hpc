from flask import Flask,render_template, jsonify, request
from mesos_hpc import mesos_hpc_start, mesos_hpc_stop
import _thread
data = 'foo'

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def hello_world():
    return render_template('hello.html')

@app.route('/stop/')
def stop():
    mesos_hpc_stop()
    return "stopped"

@app.route('/start/')
def start():
    mesos_hpc_start()
    return "started"

@app.route('/quit/')
def quit():
    stop()
    if request:
        func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "dead"


def flask():
    app.run(debug=False, port=5000, host='127.0.0.1')

if __name__ == "__main__":
    print("Starting Flask")
    flask()


import atexit
atexit.register(quit)