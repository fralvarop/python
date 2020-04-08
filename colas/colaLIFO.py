#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
lifo = Queue.LifoQueue()
for i in range(5):
    lifo.put(i)
while not lifo.empty():
    print lifo.get()

