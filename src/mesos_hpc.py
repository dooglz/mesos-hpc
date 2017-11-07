from mesoshttp.client import MesosClient
from hpc_job import mesos_hpc_buildJob
from datetime import datetime
import uuid
import sys
import threading

# MESOS_MASTER = 'http://146.176.164.62:5050'
MESOS_MASTER = 'http://127.0.0.1:5050'
jc = 1

pending_jobs = []

class HpcFramework(object):
    messages = []
    to_be_scheduled = []
    scheduled = []

    def fprint(self, msg):
        msg = str(datetime.now()) + " HPC: " + msg
        self.messages.append(msg)
        print(msg)

    class MesosFramework(threading.Thread):

        def __init__(self, client):
            threading.Thread.__init__(self)
            self.client = client
            self.stop = False

        def run(self):
            try:
                self.client.register()
            except KeyboardInterrupt:
                self.fprint('Stop requested by user, stopping framework....')

    running = False

    def __init__(self):
        self.fprint("init")

    def start(self):
        self.fprint("Start, connecting to:" + MESOS_MASTER)
        self.driver = None
        self.client = MesosClient(mesos_urls=[MESOS_MASTER])
        self.client.on(MesosClient.SUBSCRIBED, self.subscribed)
        self.client.on(MesosClient.OFFERS, self.offer_received)
        self.client.on(MesosClient.UPDATE, self.status_update)
        self.client.frameworkName = "HPC Framework"
        self.th = HpcFramework.MesosFramework(self.client)
        self.th.start()
        while self.th.isAlive():
            try:
                self.running = True
                self.th.join(1)
            except Exception as e:
                self.fprint("mesos framework exception" + str(e))
        self.running = False
        self.fprint("mesos framework stopped")

    def shutdown(self):
        self.fprint("shutdown")
        self.driver.tearDown()
        self.client.stop = True
        self.stop = True

    def subscribed(self, driver):
        self.fprint("subscribed")
        self.driver = driver

    def status_update(self, update):
        stat = update['status']
        state = stat['state']
        job = next(x for x in self.scheduled if x['task_id']['value'] == stat['task_id']['value'])

        self.fprint("status_update " + stat['task_id']['value'][:4] + " " + str(
            stat['state']))  # + " " + str(stat.get('message', {})))
        if state == "TASK_STARTING":
            pass
        elif state == "TASK_RUNNING":
            pass
        elif state == "TASK_FINISHED":
            self.scheduled.remove(job)
            pending_jobs.append(job)
        elif state == "TASK_FAILED":
            pass
        elif state == "TASK_KILLED":
            pass
        elif state == "TASK_ERROR":
            pass
        elif state == "TASK_DROPPED":
            pass
        elif state == "TASK_UNREACHABLE":
            pass
        else:
            self.fprint("unkown task state" + state)

    def compatible_offer(self, job, offer):
        of = offer.get_offer()
        for reqres in job['resources']:
            if reqres['type'] == "SCALAR":
                for avres in (x for x in of['resources'] if x['name'] == reqres['name']):
                    if reqres['scalar']['value'] > avres['scalar']['value']:
                        self.fprint(reqres['name'] + ": " + str(reqres['scalar']['value'])
                                    + "incompatible with offer " + str(avres['scalar']['value']))
                        return False
            elif reqres['type'] == "RANGES":
                self.fprint("TODO: Check ranges requirements")
            else:
                self.fprint("Unkown/invalid resource type: " + str(reqres['type']))
                return False
        return True

    def offer_received(self, offers):
        self.fprint("offer_received" + (str(offers)))
        for offer in offers:
            if len(self.to_be_scheduled) > 0 and self.compatible_offer(self.to_be_scheduled[0], offer):
                job = self.to_be_scheduled[0]
                self.fprint("Scheduling  " + job['task_id']['value'][:4])
                self.to_be_scheduled.remove(job)
                self.scheduled.append(job)
                self.run_job(job, offer)
            else:
                offer.decline()

    def run_job(self, job, mesos_offer):
        offer = mesos_offer.get_offer()
        self.fprint("run_job: " + job['task_id']['value'][:4] + " on " + offer['hostname'])
        job['agent_id']['value'] = offer['agent_id']['value']
        mesos_offer.accept([job])


test_mesos = HpcFramework()

def mesos_hpc_start():
    if (not test_mesos.running):
        threading.Thread(target=test_mesos.start).start()
    else:
        test_mesos.fprint("framework already started")


def mesos_hpc_stop():
    if (test_mesos.running):
        test_mesos.shutdown()
    else:
        test_mesos.fprint("framework not running")


def mesos_hpc_messages():
    return test_mesos.messages


def mesos_hpc_build_job():
    global jc
    task_id = str(uuid.uuid4().hex)
    job = mesos_hpc_buildJob("cooljob"+str(jc), "echo hello world from:" + task_id[:4], 0.1, 10, task_id, 0)
    pending_jobs.append(job)
    jc+=1
    return job;





def mesos_schedule_job(job=None):
    if job is None:
        job = pending_jobs[0]
    test_mesos.fprint("preparing job: " + job['task_id']['value'][:4] + " for scheduling")
    pending_jobs.remove(job)
    test_mesos.to_be_scheduled.append(job)


def mesos_hpc_getJobs():
    return {"pending": pending_jobs, "scheduling": test_mesos.to_be_scheduled, "scheduled": test_mesos.scheduled}
