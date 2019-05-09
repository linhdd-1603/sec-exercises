#!/usr/bin/python
import os
import struct
import SocketServer
import time
import random

TOTAL_LEVEL = 500
MAX_TIME = 5


class ProblemHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        self.level = 0
        self.tried = 0
        self.wfile.write("> Feeling Lucky ? <\n\n")
        self.wfile.write(
            "Can you read my mind?\nPredict %s numbers consecutive correctly and I'll give you flag.\n" % TOTAL_LEVEL)
        while True:
            my_answer = random.getrandbits(32)
            self.wfile.write("[%s/%s] What is my number?: " %
                             (self.level, self.tried))
            self.last_time = time.time()
            data = self.rfile.readline().strip()
            if not data:
                break
            try:
                if self.last_time + MAX_TIME < time.time():
                    self.wfile.write(
                        "You're not fast enough!\n")
                    break
                self.last_time = time.time()
                your_answer = int(data)
                if my_answer == your_answer:
                    if self.level == TOTAL_LEVEL:
                        flag_path = os.path.join(os.path.dirname(
                            os.path.realpath(__file__)), 'flag')
                        self.wfile.write(open(flag_path, "r").read())
                        break
                    else:
                        self.wfile.write(
                            "\nNot bad! Next, plz\n")
                        self.level += 1
                else:
                    self.wfile.write(
                        "\nBad luck, my number is %s, plz try again!\n" % my_answer)
                    self.tried += 1
            except Exception as e:
                self.wfile.write(
                    "\nIt seems we don't speak the same language!\n")
                break


class ReusableTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 2017
    SocketServer.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer((HOST, PORT), ProblemHandler)
    server.serve_forever()
