import socket  # Import socket module
import subprocess

vals = []

class Sensor:

    def __init__(self):
        #start simulator and set a wait for it to load then initiate the rest of the file
        subprocess.Popen("physense_sim")

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.port = 12345  # Reserve a port for your service.


        self.r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rport = 6666
        self.r.bind((self.host, self.rport))


    #send data
    def output(self, led, status):

        #TEST IN HERE FOR VALID ARGUMENTS try- catch
        led = str(led)
        status = str(status)

        vals = led + "," + status

        self.s.sendto((vals).encode('utf-8'), (self.host, self.port))

    def input(self, phyObj):
        self.readValues()

        if(phyObj == "Button_1" and vals[4] == "1"):
           return "pressed"

        elif(phyObj == "Button_2" and vals[5] == "1"):
            return "pressed"

        elif (phyObj == "Button_3" and vals[6] == "1"):
            return "pressed"

        elif (phyObj == "Button_4" and vals[7] == "1"):
            return "pressed"

        elif (phyObj == "light"):
            if vals[0] == "0":
                return "off"
            else:
                return "on"

        elif (phyObj == "temp"):
           return int(vals[1] + vals[2] + vals[3])

    def readValues(self):
        temp, a = self.r.recvfrom(1024)  # once it receives this value that's it. so store in variable
        self.s.sendto(("test").encode('utf-8'), (self.host, self.port))

        temp = str(temp)

        temp = temp.strip('b')
        temp = temp.strip("\'")
        temp = temp.strip("\'")

        global vals
        vals = temp