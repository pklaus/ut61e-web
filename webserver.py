#!/usr/bin/env python3

from ut61e import es51922
from bottle import route, run, view, redirect, static_file
import json
import socket
import threading 
import logging

UDP_IP = "localhost"
UDP_PORT = 5005

class UdpReceiver(threading.Thread): 
    def __init__(self, host, port): 
        threading.Thread.__init__(self) 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.results = dict()
 
    def run(self): 
        while True:
           data, addr = self.sock.recvfrom(256) # buffer size is 256 bytes
           data = data.strip()
           try:
               data.decode('ascii')
           except:
               logging.warning('Not an ASCII input line, ignoring: "{}"'.format(data))
               continue
           if len(data)==12:
               try:
                   results = es51922.parse(data, True)
               except Exception as e:
                   logging.warning('Error "{}" packet from multimeter: "{}"'.format(e, data))
                   continue
               del results['packet_details']['raw_data_binary']
               self.results = results
           elif data:
               logging.warning('Unknown packet from multimeter: "{}"'.format(data))
 
datasource = UdpReceiver(UDP_IP, UDP_PORT)
datasource.start() 

@route('/api/get_status')
def get_status():
    return datasource.results

@route('/')
def refer():
    #redirect('/api/get_status')
    return static_file('UT61E_Display.html', root='./')

@route('/images/<path:path>')
def callback(path):
    return static_file(path, root='./images/')

run(host='localhost', port=8080, debug=True)

