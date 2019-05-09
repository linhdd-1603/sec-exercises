
import os
import struct
import SocketServer
import time
import random
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, getStrongPrime
import sys
from secret import flag

p = getStrongPrime(512)
q = getStrongPrime(512)
e = 65537


class Server():
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.e = e
        self.N = p*q
        phi = (p-1)*(q-1)
        self.d = inverse(self.e, phi)
        self.enc_flag = pow(bytes_to_long(flag), self.e, self.N)

    def encrypt(self, message):
        if len(message) < 10:
            return False, "Your message is too short"
        m = bytes_to_long(message)
        if m >= self.N:
            return False, "Your message is too long"
        else:
            c = pow(m, self.e, self.N)
            c_flag = (pow(c, m, self.N) * self.enc_flag) % self.N
            return c, c_flag

    def decrypt(self, cipher):
        cipher = int(cipher)
        message = pow(cipher, self.d, self.N)
        return message


class ProblemHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.server = Server(p, q)
        self.banner = "="*10 + "KoMA RSA service 4..0" + "="*10
        self.menu = "1. Encrypt\n2. Decrypt\n3. Exit\n4. Publickey\n"

        self.wfile.write(self.banner)
        while 1:
            try:
                self.wfile.write(self.menu)
                self.wfile.write("Your choice: ")
                choice = int(self.rfile.readline().strip())
                if choice == 1:
                    self.wfile.write("Your message: ")
                    message = self.rfile.readline().strip()
                    cipher, cipher_flag = self.server.encrypt(message)
                    if cipher:
                        self.wfile.write("Your cipher: %d\n" % cipher)
                        self.wfile.write(
                            "Your cipher_flag: %d\n" % cipher_flag)
                    else:
                        self.wfile.write("%s\n" % cipher_flag)
                elif choice == 2:
                    self.wfile.write("Your cipher: ")
                    cipher = self.rfile.readline().strip()
                    message = self.server.decrypt(cipher)
                    self.wfile.write("Decrypted message: %d\n" % message)
                elif choice == 3:
                    self.wfile.write("Thanks for using my service.\n")
                    break
                elif choice == 4:
                    self.wfile.write(
                        "Pubkey: {\"N\": %d, \"e\":%d}\n" % (self.server.N, self.server.e))
                else:
                    self.wfile.write("Invalid choice")
            except Exception as e:
                print e
                import traceback
                traceback.print_exc()
                self.wfile.write("Bad input\n")
                break


class ReusableTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 2018
    SocketServer.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer((HOST, PORT), ProblemHandler)
    server.serve_forever()
