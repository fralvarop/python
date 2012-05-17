#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue

colaPrioridad = Queue.PriorityQueue()
colaPrioridad.put((3, 'medium 1'))
colaPrioridad.put((4, 'medium 2'))
colaPrioridad.put((10, 'low'))
colaPrioridad.put((1, 'high'))

while not colaPrioridad.empty():
    siguiente = colaPrioridad.get()
    print siguiente
    print siguiente[1]

