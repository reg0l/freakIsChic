#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, os, sys, select
import argparse 
from OpenSSL import SSL
from multiprocessing import Pool
import signal
import time

class Timeout():
    """Issue with the methode set_timeout in Pyopenssl create a timeout function only working on Unix system"""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

class FreakisChic(object):
	def __init__(self, host, port):
		self._host = host
		self._port = port
	def connexion(self):
		_context = SSL.Context(SSL.TLSv1_METHOD)
		_context.set_options(SSL.OP_NO_SSLv2)
		_context.set_cipher_list('EXPORT')
		_sock = socket.socket()
		ssl_sock = SSL.Connection(_context, _sock)
		try:	
			with Timeout(1):	
				ssl_sock.connect((self._host, self._port))
		except Timeout.Timeout:
			ssl_sock.close()
			return False
		else:
			return ssl_sock
	def VulnCheck(self, socket):
		self._socket = socket 
		try:		
			self._socket.do_handshake()
		except SSL.Error:
			return	self._host, self._port, 'NOT VULNERABLE'
		else:
			return	self._host, self._port, 'VULNERABLE'
		
	def range_ip(self, range_ip):
		self._list_ip = []
		self._ip = 0
		#while i < 
		
def main():
	parser = argparse.ArgumentParser("Check if hostname give in argument is vulnerable to FREAK")
	parser.add_argument("--host", help="hostname you wants to check. If you ghave more than 1 host please separate it by a space", action='store', nargs= '+')
	parser.add_argument("--port", help="Port running the service ", type=int, default='443', action='store')
	args = parser.parse_args()
	if args.host:
		for host in args.host:			
			obj = FreakisChic(host, args.port)
			socket = obj.connexion()
			if socket == False:
				print 'Your host %s at port: %s is UNREACHABLE' %(host, args.port)
			else:
				retour = obj.VulnCheck(socket)
				print 'Your host %s at port: %s is %s' %(retour[0], retour[1], retour[2])
			
if __name__ == "__main__":
    main()
