import time
import ujson
from simple import MQTTClient
from machine import Pin, Timer

from chipid import chipid
from wakeup import WAKE_ON_LINE
# from nettime import getformattime


class mqtt:
    def __init__(self,oled, client_id='', username='', password='',macs=[],BROADCAST_IP='192.168.1.255',BROADCAST_PORT=40000):
        self.failed_count = 0
        self.oled = oled
        self.server = "183.230.40.39"
        self.client_id = client_id
        self.username = username
        self.password = password
        self.topic = (chipid() + '-sub').encode('ascii') if client_id == '' else (client_id + '-' + chipid() + '-sub').encode('ascii')
        self.mqttClient = MQTTClient(self.client_id, self.server,6002,self.username,self.password)
        self.wakeonline = WAKE_ON_LINE(macs,BROADCAST_IP,BROADCAST_PORT)
        # self.pid = 0 # publish count

    # def pubData(self, t):
    #     value = {'datastreams':[{"id":"temp","datapoints":[{"value":1}]}]}
    #     jdata = ujson.dumps(value)
    #     jlen = len(jdata)
    #     bdata = bytearray(jlen+3)
    #     bdata[0] = 1 # publish data in type of json
    #     bdata[1] = int(jlen / 256) # data lenght
    #     bdata[2] = jlen % 256      # data lenght
    #     bdata[3:jlen+4] = jdata.encode('ascii') # json data
    #     #print(bdata)
    #     print('publish data', str(self.pid + 1))
    #     try:
    #         self.mqttClient.publish('$dp', bdata)
    #         self.pid += 1
    #         self.failed_count = 0
    #     except Exception as ex:
    #         self.failed_count += 1
    #         print('publish failed:', ex.message())
    #         if self.failed_count >= 3:
    #             print('publish failed three times, esp resetting...')
    #             reset()

    def sub_callback(self, topic, msg):
        # print((topic,msg))
        cmd = msg.decode()
        if cmd == 'wakeup':
            self.oled.write_lines(line2='send wol package...')
            # self.oled.write_lines(line3=getformattime())
            self.wakeonline.send()
            # self.oled.write_lines(line4=getformattime())
            self.oled.write_lines(line2='')

    def ping(self,t):
        self.mqttClient.ping()

    def connect(self):
        self.mqttClient.set_callback(self.sub_callback)
        self.mqttClient.connect()
        tim = Timer(-1)
        tim.init(period=30000, mode=Timer.PERIODIC, callback=self.ping) #Timer.PERIODIC   Timer.ONE_SHOT
        self.mqttClient.subscribe(self.topic)
        print("Connected to %s, subscribed to %s topic." % (self.server, self.topic))
        try:
            while 1:
                #self.mqttClient.wait_msg()
                msg = self.mqttClient.check_msg()
                print (msg)
        finally:
            #self.mqttClient.unsubscribe(self.topic)
            self.mqttClient.disconnect()
            print('mqtt closed')
            tim.deinit()
