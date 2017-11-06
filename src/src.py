from flask import Flask,render_template, jsonify, request
from mesos_hpc import mesos_hpc_start, mesos_hpc_stop, mesos_hpc_messages, mesos_hpc_build_job, mesos_hpc_getJobs, mesos_schedule_job

import subprocess
from datetime import datetime
import _thread

startTime = datetime.now()
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('hello.html', version=githash, startTime=startTime)

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

@app.route('/messages',methods=['GET'])
def messages():
    return jsonify(mesos_hpc_messages())

@app.route('/jobs',methods=['GET'])
def jobs():
    return jsonify(mesos_hpc_getJobs())

@app.route('/build',methods=['GET','POST'])
def build():
    return jsonify(mesos_hpc_build_job())

@app.route('/schedule',methods=['GET','POST'])
def schedule():
    return jsonify(mesos_schedule_job())


def flask():
    app.run(debug=False, port=5000, host='127.0.0.1')

try:
    githash =  subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
except Exception:
    githash = "?"

if __name__ == "__main__":
    print("Starting Flask")
    flask()


import atexit
atexit.register(quit)