#/usr/bin/env python
# -*- coding: UTF-8 -*-
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
from pocoui_lib.android import kotoList
from pocoui_lib.android import kotoPage
import random


def swipe_find(poco1,precent):
    #找不到元素像下滑动屏幕
    while poco1.exists()==False:
        print("not exist...")
        poco().swipe(precent)
    else:
        print("exist...")
        return poco1

def multi_select_poco_point_item(pocoPoint,count):
    #列表多选,入参count为多选数量
    table = pocoPoint
    table.wait(timeout=10)
    itemlist =table.child()
    counts = len(list(itemlist))
    a = random.sample(range(0,counts),count)    #选择0到counts-1中，不重复数count次
    for i in a:
        itemlist[i].click()
        pocoPoint.swipe([0,-0.5])
        j = i+1
        print("select the %s " %j)


def all_poco_point_item(pocoPoint):
    # 选择列表所有选项
    table = pocoPoint
    table.wait(timeout=10)
    itemlist =table.child()
    # 可能会造成 Click position out of screen
    count = len(list(itemlist))
    print("=================success")
    print(count)
    print("=================success")
    for i in range(0,count):
    	itemlist[i].click()
    # try:
    #     itemlist[index].click()
    # except PocoNoSuchNodeException:
    #     print('list not exist item[%d]' % (index))
# #时间控件，滚动年、月
# def time(pocoy):
# 	for i in range(3,8):
# 		pocoy.swipe([0.1,-0.1])
# 	print("=================success")
