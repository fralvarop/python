#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
fifo = Queue.Queue(12)
for i in range(13):
    if not fifo.full():
        fifo.put(i)
while not fifo.empty():
    print fifo.get()

