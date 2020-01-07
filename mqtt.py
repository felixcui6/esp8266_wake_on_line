import time
import ujson
from simple import MQTTClient
from machine import Pin, Timer

from chipid import chipid
from wakeup import WAKE_ON_LINE
# from nettime import getformattime
from status import check_status


class mqtt:
    def __init__(self,oled, client_id='', username='', password='',macs=[],BROADCAST_IP='192.168.1.255',BROADCAST_PORT=40000):
        self.failed_count = 0
        self.oled = oled
        self.cs = check_status(oled=oled)
        self.server = "183.230.40.39"
        self.client_id = client_id
        self.username = username
        self.password = password
        self.topic = (chipid() + '-sub').encode('ascii') if client_id == '' else (client_id + '-' + chipid() + '-sub').encode('ascii')
        self.mqttClient = MQTTClient(self.client_id, self.server,6002,self.username,self.password)
        self.wakeonline = WAKE_ON_LINE(macs,BROADCAST_IP,BROADCAST_PORT)

    def sub_callback(self, topic, msg):
        cmd = msg.decode()
        if cmd == 'wakeup':
            self.oled.write_lines(line2='send wol package...')
            self.wakeonline.send()
            self.oled.write_lines(line2='')

    def ping(self,t):
        self.mqttClient.ping()
        self.cs.display_status()

    def connect(self):
        self.mqttClient.set_callback(self.sub_callback)
        self.mqttClient.connect()
        tim = Timer(-1)
        tim.init(period=30000, mode=Timer.PERIODIC, callback=self.ping) #Timer.PERIODIC   Timer.ONE_SHOT
        self.mqttClient.subscribe(self.topic)
        # print("Connected to %s, subscribed to %s topic." % (self.server, self.topic))
        try:
            while 1:
                msg = self.mqttClient.check_msg()
                print (msg)
        finally:
            self.mqttClient.disconnect()
            print('mqtt closed')
            tim.deinit()
