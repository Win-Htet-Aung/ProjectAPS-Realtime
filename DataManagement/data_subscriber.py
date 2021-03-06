from google.cloud import pubsub
from DataManagement.models import *
import os
import json
import datetime

pdir = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(pdir, "MyIoT-61c1e4f98fcf.json")

class Handler:
    def __init__(self):
        self.project_id = "myiot-297607"
        self.subscription_id = "projectaps"
        self.subscriber = pubsub.SubscriberClient()
        self.sub_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)
        self.subscriber.subscribe(self.sub_path, callback = self.callback)
        print("subscribed!")

    def callback(self, message):
        resp = message.data
        data = resp.decode("UTF-8")
        print(data)
        try:
            data = json.loads(data)
        except:
            print('invalid format :', data)
        else:
            serial = data['serial']
            sensor = Sensor.objects.get(serial = serial)
            now = datetime.datetime.fromtimestamp(data['timestamp'])
            hour, minute = now.hour, now.minute
            label = f"{hour}:{minute}"
            TPLog(sensor=sensor, loggedtime=now, temp=data['temp']).save()
            print('saved')
        finally:
            message.ack()

handler = Handler()
