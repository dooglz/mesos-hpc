from mesoshttp.client import MesosClient
import sys
import threading

def fprint(str):
    print("HPC:" + str)

class HpcFramework(object):
    class MesosFramework(threading.Thread):

        def __init__(self, client):
            threading.Thread.__init__(self)
            self.client = client
            self.stop = False

        def run(self):
            try:
                self.client.register()
            except KeyboardInterrupt:
                fprint('Stop requested by user, stopping framework....')

    running = False
    def __init__(self):
        fprint("init")

    def start(self):
        fprint("start")
        self.driver = None
        self.client = MesosClient(mesos_urls=['http://127.0.0.1:5050'])
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
                fprint("mesos framework exception" +str(e))
        self.running = False
        fprint("mesos framework stopped")

    def shutdown(self):
        fprint("shutdown")
        self.driver.tearDown()
        self.client.stop = True
        self.stop = True

    def subscribed(self, driver):
        fprint("subscribed")
        self.driver = driver

    def status_update(self, update):
        fprint("status_update {}".format(update['status']['state']))

    def offer_received(self, offers):
        fprint("offer_received" + (str(offers)))
        for offer in offers:
            offer.decline()

    def run_job(self, mesos_offer):
        fprint("run_job")

test_mesos = HpcFramework()


def mesos_hpc_start():
    if(not test_mesos.running):
        threading.Thread(target=test_mesos.start).start()
    else:
        fprint("framework already started")

def mesos_hpc_stop():
    if (test_mesos.running):
        test_mesos.shutdown()
    else:
        fprint("framework not running")


