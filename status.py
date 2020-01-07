import time
from sh1106 import OLED

class check_status:
    def __init__(self,oled):
        self.oled = oled
        self.count = 1
        self.string = list('0 1 2 3 4 5 6 7 8 9 0')

    def display_status(self):
        self.oled.write_lines(line8=''.join(self.string))
        if self.count >= 40:
            self.count = 1
        if self.count < 20:
            self.string[self.count] = '>'
        else:
            self.string[40 - self.count] = '<'
        self.count += 2

if __name__ == '__main__':
    oled = OLED()
    cs = check_status(oled=oled)
    while True:
        cs.display_status()
        time.sleep(1)
