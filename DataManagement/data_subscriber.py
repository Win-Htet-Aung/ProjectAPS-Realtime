from google.cloud import pubsub
import os
import json
import requests
import websocket
import time
import random
import datetime

pdir = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = pdir + "\\MyIoT-61c1e4f98fcf.json"

class Handler:
    def __init__(self):
        self.project_id = "myiot-297607"
        self.subscription_id = "projectaps"
        self.subscriber = pubsub.SubscriberClient()
        self.sub_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)
        self.subscriber.subscribe(self.sub_path, callback = self.callback)
        self.ws = websocket.WebSocket()
        # print("subscribed!")

    def callback(self, message):
        self.ws.connect("ws://localhost:8000/ws/dataplotter/S3001/")
        now = datetime.datetime.now()
        hour, minute = now.hour, now.minute
        label = f"{hour}:{minute}"
        resp = message.data
        data = resp.decode("UTF-8")
        data = json.loads(data)
        self.ws.send(json.dumps({'label':label, 'temp':data['temp']}))
        message.ack()
        self.ws.close()

handler = Handler()
