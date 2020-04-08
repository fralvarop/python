#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cliente1.py
import socket
soc = socket.socket()
hostname = socket.gethostname()
puerto = 21000
soc.connect((hostname, puerto))
print soc.recv(1024)
soc.close

