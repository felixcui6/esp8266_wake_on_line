import ntptime
import utime
from machine import Timer


def synctime(t):
    try:
        ntptime.time()
        ntptime.settime()
    except:
        pass


def autosynctime():
    tim = Timer(-1)
    tim.init(period=30000, mode=Timer.PERIODIC, callback=synctime)  # Timer.PERIODIC   Timer.ONE_SHOT


def getformattime():
    (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
    return str(year) + '-' + '%02d' % month + '-', '%02d' % mday + ' ' + '%2d' % hour + ':' + '%02d' % minute + ':' + '%02d' % second
