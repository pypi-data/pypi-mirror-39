#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
def random_Swipe(nodeName,childNode):
    node = nodeName
    item = node.child()
    if item.exists():
        count = len(list(item))
        print(count)
        print("***Ding!***")
        try:
            item[random.randint(0,count)].click()
            print("***Bingo!***")
        except PocoNoSuchNodeException:
            print('No item')
def random_Swipe1(nodeName):
    node = nodeName.child()
    #item = poco("node")
    if node.exists():
        count = len(list(node))
        print(count)
        print("***Ding!***")
        #node([random.randint(0,count)]).click()
        try:
            node[random.randint(0,count-1)].click()
            print("***Bingo!***")
        except PocoNoSuchNodeException:
            print('No item')