from mesoshttp.client import MesosClient
import sys
import threading

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
                print('Stop requested by user, stopping framework....')


    def __init__(self):
        print("init")

    def start(self):
        print("start")
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
                self.th.join(1)
            except Exception as e:
                print("mesos framework exception" +str(e))
        print("mesos framework stopped")

    def shutdown(self):
        print("shutdown")
        self.driver.tearDown()
        self.client.stop = True
        self.stop = True

    def subscribed(self, driver):
        print("subscribed")
        self.driver = driver

    def status_update(self, update):
        print("status_update {}".format(update['status']['state']))

    def offer_received(self, offers):
        print("offer_received" + (str(offers)))
        for offer in offers:
            offer.decline()

    def run_job(self, mesos_offer):
        print("run_job")

test_mesos = HpcFramework()

def mesos_hpc():
    print ("where are the nuclear wessels?")
    threading.Thread(target=test_mesos.start).start()
    return 'goodbye World!'

def mesos_hpc_stop():
    test_mesos.shutdown()