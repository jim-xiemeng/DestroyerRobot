#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/24 15:30
# @Author  : vivid
# @Email   : 331597811@163.com
# @File    : test01.py
from DestroyerRobot.automation.util.MySqlDBUtil import MysqlDB
from DestroyerRobot.automation.util.Regex import Reg
import time
import csv
sql = "show tables "
dbs = MysqlDB().queryOperation(sql)
nums = dbs[0].__len__()

for i in range(0,nums):
    lists = []
    print(i)
    tablename = dbs[0][i][0]
    tablelist = ["build_ specialist","role","resc_role"]
    if tablename not in  tablelist:
        sql = " show create table %s" %tablename
        info = MysqlDB().querydict(sql)
        commentStr = info[0]['Create Table']
        commect = Reg().fetchStringByBoundary(commentStr,LB="COMMENT='",RB="'")
        print(info[0]["Table"])
        lists.append(info[0]['Table'])
        lists.append(commect)
        out = open("C:\\Users\\vivid\Desktop\\example_stats.csv","a",newline="")
        cvs_writer = csv.writer(out,dialect="excel")
        cvs_writer.writerow(lists)
        time.sleep(0.5)



# row = ['5',"haiiii","123421","2fw"]
# out = open("C:\\Users\\vivid\Desktop\\example_stats.csv","a",newline="")
# cvs_writer = csv.writer(out,dialect="excel")
# cvs_writer.writerow(row)

