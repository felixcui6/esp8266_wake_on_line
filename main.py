import uos
import ujson
import time
import machine
from machine import Timer

from sh1106 import OLED
from wifi import apmode,connect_wifi
from web import webserver
from chipid import chipid
from mqtt import mqtt
# from nettime import autosynctime

macs = ['XXX'] # 要唤醒设备的MAC地址,['00-00-00-00-00-00']
BROADCAST_PORT = 40000

product_id = 'XXX' # 产品ID
client_id = 'XXX' # 设备ID
authinfo = 'XXX' # 鉴权信息

wifi_name = "ESP8266_" + chipid()
wifi_password = "1234567890"


def main():
    oled = OLED()
    oled.write_lines(line1='start...')
    currdir = uos.getcwd()
    files = uos.listdir(currdir)
    if ('config.ini' in files):
        fconfig = open(currdir + 'config.ini', 'r')
        configdic = ujson.loads(fconfig.read())
        fconfig.close()
        oled.write_lines(line2='connecting to network...')
        flag,wifi_status,esp8266_ip = connect_wifi(configdic['WiFiName'], configdic['WiFiPasswd'])
        if flag:
            oled.write_lines(line1='ip:'+esp8266_ip,line2='',line3='')
        else:
            oled.write_lines(line3='connect network failed, restarting...')
            if wifi_status == 2 or wifi_status == 3:
                uos.remove(currdir + 'config.ini')
            machine.reset()
    else:
        esp8266_ip = apmode(wifi_name,wifi_password)
        oled.write_lines(line1='wifi:'+wifi_name,line2='pswd:'+wifi_password,line3='ip  :'+esp8266_ip)
        webserver()

    # autosynctime()

    BROADCAST_IP = esp8266_ip[:esp8266_ip.rfind('.')] + '.255'
    mq = mqtt(oled=oled,client_id=client_id, username=product_id, password=authinfo,macs=macs,BROADCAST_IP=BROADCAST_IP,BROADCAST_PORT=BROADCAST_PORT)
    while True:
        mq.connect()
        time.sleep(30)


if __name__ == '__main__':
    # tim = Timer(-1)
    # tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t: ShowSensorData())
    main()

