#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, os, sys, select
import argparse 
from OpenSSL import SSL

class FreakisChic(object):
	def __init__(self, host, port):
		self._host = host
		self._port = port
	def connexion(self):
		print 'Trting vulnerabilities freak for: %s %s' %(self._host, self._port)
		context = SSL.Context(SSL.TLSv1_METHOD)
		context.set_options(SSL.OP_NO_SSLv2)
		context.set_cipher_list('EXPORT')
		sock = socket.socket()
		ssl_sock = SSL.Connection(context, sock)
		ssl_sock.connect((self._host, self._port))
		try:		
			ssl_sock.do_handshake()
		except SSL.Error:
			print 'The host: %s is not vulnerable to FREAK vuln' %(self._host)
		else:
			print 'you server %s is vulnerable to FREAK' %(self._host)
def main():
	parser = argparse.ArgumentParser("Check if hostname give in argument is vulnerable to FREAK")
	parser.add_argument("--host", help="hostname you wants to check", action='store')
	parser.add_argument("--port", help="Port running the service ", type=int, default='443', action='store')
	parser.add_argument("--check", help="Check for freak vulnerability", action='store_true')
	args = parser.parse_args()
	
	if args.check:
		obj = FreakisChic(args.host, args.port)
		obj.connexion()
if __name__ == "__main__":
    main()
