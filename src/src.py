from flask import Flask,render_template, jsonify, request
from mesos_hpc import mesos_hpc, mesos_hpc_stop
import _thread
data = 'foo'

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def hello_world():
    print(str(request.values))
    return render_template('hello.html')

@app.route('/stop/')
def ms():
    mesos_hpc_stop()
    return "stopped"

@app.route('/start/')
def mst():
    mesos_hpc()
    return "started"

def flask():
    app.run(debug=False, port=5000, host='127.0.0.1')

if __name__ == "__main__":
    print("yo")
    flask()
    print("yolo")



