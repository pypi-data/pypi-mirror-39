from datetime import datetime

class Target:

    def __init__(self, ipv4, mac = '', manu = ''):

        self.ipv4 = ipv4
        self.mac = mac
        self.manu = manu
        self.ts = datetime.now()
