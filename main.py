#!/usr/bin/python3
import libvirt
from lib.LifecycleUtilities import *
from lib.StatusUtilites import *

#print(boot("centos"))
#shutdown("test-vm")
#reboot("centos")

print(destory("t2ee-c1","centos"))