#!/usr/bin/python
 # -*- coding: utf-8 -*-


import tnthai.segment as tn

f = open("decodeignore", "r")
decodeignore = "".join(f.readlines())
f.close()

f = open("filteredtext", "r")
filteredtext = "".join(f.readlines())
f.close()

f = open("rawpdftext", "r")
rawpdftext = "".join(f.readlines())
f.close()

print tn.UnsafeSegment(decodeignore)