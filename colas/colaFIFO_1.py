#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
fifo = Queue.Queue()
for i in range(5):
    fifo.put(i)
while not fifo.empty():
    print fifo.get()

