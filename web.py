import machine
import socket
import ujson
import uos
import time

def webserver():
    configlist = ['WiFiName', 'WiFiPasswd']
    configdic = {}
    html = """<!DOCTYPE html>
        <html>
            <head> <title>ESP8266 Web Config</title> </head>
            <body> <h1>ESP8266 Web Config</h1>
                %s
                <table>
                    <FORM action="" method="GET">
                        %s%s
                    </form>
                </table>

            </body>
        </html>
        """
    row1 = ['<tr><td>%s</td><td><input type=\"text\" name=\"%s\" value=""></td></tr>' % (key,key) for key in configlist]
    row2 = ['<tr><td></td><td><input type=\"submit\" value=\"SAVE\"></td></tr>']
    row3 = ['<tr><span style="color:red">Save Config to ESP8266</span></tr>']
    row4 = ['<tr><span style="color:red">Config Error</span></tr>']

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)
    flag = 0
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:

            line = cl_file.readline()
            print(line,type(line))
            if not line or line == b'\r\n':
                break
            else:
                configline = line.decode().split(' ')[1]
                if(configline[:2] == '/?'):
                    configdic = {k: v for k, v in (l.split('=', 1) for l in configline[2:].split('&'))}
                    if('' not in configdic.values()):
                        flag = 1
                    else:
                        flag = -1
        if(flag == 1):
            response = html % ('\n'.join(row3), '\n'.join(row1), '\n'.join(row2))
            currdir = uos.getcwd()
            fconfig = open(currdir + 'config.ini', 'w')
            fconfig.write(ujson.dumps(configdic))
            fconfig.flush()
            fconfig.close()
        elif(flag == -1):
            response = html % ('\n'.join(row4), '\n'.join(row1), '\n'.join(row2))
        else:
            response = html % ('\n', '\n'.join(row1), '\n'.join(row2))
        cl.send(response)
        cl.close()
        if(flag == 1):
            time.sleep(5)
            machine.reset()
