import datetime
import socket
import threading


class ConnProcessor(threading.Thread):
    """ A Thread is created with every incoming connection """
    id = None

    def __init__(self, client, addr, db):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr
        self.db = db
        self.should_terminate = False

    def run(self):
        print(">>>Connection from {}:{}".format(self.addr[0], self.addr[1]), flush=True)
        self.client.settimeout(120)

        while True:
            if self.should_terminate:
                break

            try:
                data = self.client.recv(1024)
            except socket.timeout:
                if self.id:
                    self.send_message("({}AP01HSO)".format(self.id))
            else:
                if data:
                    self.process_message(data.decode('ascii'))
                else:
                    print("no msg!")
                    break

        print(">>>finished", flush=True)
        self.client.close()

    def process_message(self, msg):
        if len(msg) < 19 or msg[0] != '(' or msg[len(msg) - 1] != ")":
            print("invalid msg:", msg)
            return

        print("[{}] got msg: {}".format(datetime.datetime.now(), msg))
        self.id = msg[1:13]
        command = msg[13:17]

        # kill previous connections with this device
        for t in threading.enumerate():
            if type(t) is ConnProcessor and t is not self and t.id == self.id:
                t.should_terminate = True

        # this is the only command the gps responds to
        # self.send_message("({}AP05)".format(self.id))

        if command == "BP00":
            self.send_message("({}AP01HSO)".format(self.id))
        elif command == "BP05":
            self.send_message("({}AP05)".format(self.id))
        elif command == "BO01":
            # low battery?
            self.parse_location(msg.replace("BO018", "BO01"))
            self.send_message("({}AP01HSO)".format(self.id))
        elif command == "BR03" or command == "BR00":
            self.parse_location(msg)
            self.send_message("({}AP01HSO)".format(self.id))

    def send_message(self, msg):
        print("[{}] sending: {}".format(datetime.datetime.now(), msg), flush=True)
        self.client.sendall(bytes(msg, 'ascii'))

    def parse_location(self, msg):
        id = msg[1:13]
        date = msg[17:23]
        availability = msg[23:24]
        latitude = msg[24:33]
        latitude_ind = msg[33:34]
        longitude = msg[34:44]
        longitude_ind = msg[44:45]
        speed = msg[45:50]
        times = msg[50:56]
        orientation = msg[56:62]
        iostate = msg[62: 70]
        milepost = msg[70:71]
        milage = msg[71:79]

        date_time = '20' + date[0:2] + '-' + date[2:4] + '-' + date[4:6] + ' ' + times[0:2] + ':' + times[
                                                                                                   2:4] + ':' + times[
                                                                                                                4:6]

        latitude_dd = round(float(latitude[0:2]) + float(latitude[2:2 + 7]) / 60, 6)
        if latitude_ind != "N":
            latitude_dd = - latitude_dd

        longitude_dd = round(float(longitude[0:3]) + float(longitude[3:3 + 7]) / 60, 6)
        if longitude_ind != "E":
            longitude_dd = - longitude_dd

        maps_url = "http://www.google.com/maps/search/?api=1&query=" + str(latitude_dd) + "," + str(longitude_dd)

        print(maps_url)

        self.db.insert_location((id, latitude_dd, longitude_dd, speed, date_time, maps_url, availability, iostate))
