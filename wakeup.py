import socket
import ustruct
import time


class WAKE_ON_LINE:
    def __init__(self,macs=[],BROADCAST_IP='192.168.1.255',BROADCAST_PORT=40000):
        self.macs = macs
        self.BROADCAST_IP = BROADCAST_IP
        self.BROADCAST_PORT = BROADCAST_PORT

    def create_magic_packet(self,macaddress):
        """
        Create a magic packet which can be used for wake on lan using the
        mac address given as a parameter.
        Keyword arguments:
        :arg macaddress: the mac address that should be parsed into a magic
                         packet.
        """
        if len(macaddress) == 12:
            pass
        elif len(macaddress) == 17:
            sep = macaddress[2]
            macaddress = macaddress.replace(sep, '')
        else:
            raise ValueError('Incorrect MAC address format')

        # Pad the synchronization stream
        data = b'FFFFFFFFFFFF' + (macaddress * 16).encode()
        send_data = b''

        # Split up the hex values in pack
        for i in range(0, len(data), 2):
            send_data += ustruct.pack(b'B', int(data[i: i + 2], 16))
        return send_data

    def send_magic_packet(self):
        """
        Wakes the computer with the given mac address if wake on lan is
        enabled on that host.
        Keyword arguments:
        :arguments macs: One or more macaddresses of machines to wake.
        :key ip_address: the ip address of the host to send the magic packet
                         to (default "255.255.255.255")
        :key port: the port of the host to send the magic packet to
                   (default 9)
        """
        packets = []

        for mac in self.macs:
            packet = self.create_magic_packet(mac)
            packets.append(packet)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # sock.setsockopt(socket.SOL_SOCKET, 32, 1)
        sock.connect((self.BROADCAST_IP, self.BROADCAST_PORT))
        print(self.BROADCAST_IP,self.BROADCAST_PORT)
        for packet in packets:
            print(packet)
            sock.send(packet)
        sock.close()

    def send(self):
        try:
            self.send_magic_packet()
            time.sleep(1)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    macs = ['00-11-32-11-22-33', '70-85-C2-70-5A-51']
    BROADCAST_IP = '192.168.1.255'
    BROADCAST_PORT = 40000
    wakeonline = WAKE_ON_LINE(macs,BROADCAST_IP,BROADCAST_PORT)
    wakeonline.send()
