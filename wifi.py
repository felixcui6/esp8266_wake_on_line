import network
import web
import time

# STAT_IDLE – no connection and no activity, 0 未连接
# STAT_CONNECTING – connecting in progress,  1 连接中
# STAT_WRONG_PASSWORD – failed due to incorrect password, 2 密码错误
# STAT_NO_AP_FOUND – failed because no access point replied, 3 ssid不可用
# STAT_CONNECT_FAIL – failed due to other problems, 4 无响应
# STAT_GOT_IP – connection successful. 5 连接成功


def apmode(wifi_name,password):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid=wifi_name, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    net_config = ap_if.ifconfig()
    return net_config[0]

def connect_wifi(ssid,password):
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    for _ in range(20):
        if sta_if.isconnected():
            net_config = sta_if.ifconfig()
            return True,sta_if.status(),net_config[0]
        time.sleep(1)
    return False,sta_if.status(),''
