#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/22 13:58
# @Author  : vivid
# @Email   : 331597811@163.com
# @File    : s5.py

from locust import HttpUser,between,TaskSet,task,tag , events
from gevent._semaphore import Semaphore
import requests
import os
import threading
import time
import uuid
# all_locusts_spawned = Semaphore(0)
# all_locusts_spawned.acquire()
# def on_hatch_complete(**kwargs):
#     all_locusts_spawned.release() #创建钩子方法
#
# events.hatch_complete += on_hatch_complete #挂载到locust钩子函数（所有的Locust实例产生完成时触发）

class MarkerUser(TaskSet):
    execNum = [] #统计执行次数
    def on_start(self):

        self.headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

        }
        """
        运行时间为秒和运行次数取值都为int类型,只能唯一
        self.executeTime，执行时间;
        self.executeTimes，给定执行次数；
        self.current_time ，初始化脚本启动时间。
        """
        self.current_time = time.time()
        self.executeTime = 0 #执行时间
        self.executeTimes= 1 #执行次数

        self.req = self.markerlogin()
        # self.loadToken = self.uploadToken()
        # print("self.loadToken:",self.loadToken["data"]['imgToken'])

        # all_locusts_spawned.wait()


    def on_stop(self):
        print("stop Taskcase")

    def stop(self,currentTime=0,currentNums=0,url="http://127.0.0.1:8089/stop"):
        """
        调用此方法需要在页面中操作才可以
        currentTime，给定当前时间，判断是否则执行时间取值脚本 编写为 -->self.stop(300) or self.stop(300,0)  300为s秒
        currentNums，给定执行次数，则执行次数取值脚本 必须编写成 -->self.stop(0,50)  0不做任何统计只是占位，执行了50次请求，
        currentTime，currentNums，0,0-->self.stop(0,0) or self.stop() or self.stop(0) 0为s秒执行0请求，本次脚本停止
        url:默认写入为当前机子url地址
        判断当前执行脚本是否符合执行时长，执行次数，web终止运行脚本,当终止执行时会调用on_stop脚本，停止user携程操作
        :return:
        """
        # url = "http://127.0.0.1:8089/stop"
        if self.executeTime > 0:
            if currentTime >= self.current_time+self.executeTime:
                requests.session().get(
                    url,
                    headers = self.headers
                )
            else:
                pass
        elif self.executeTimes > 0:
            if currentNums >= self.executeTimes :
                requests.session().get(
                    url,
                    headers=self.headers
                )
            else:
                pass
        else:
            requests.session().get(
                url,
                headers=self.headers
            )


    def markerlogin(self):
        #url = https://tapi.lifeat.cn:45788/

        datas={"loginName": "15811478363", "password": "123456", "loginSysName": "bonus"}
        # with self.client.post(url="/user/login/login",
        #                       json=datas,
        #                       headers=self.headers,
        #                       catch_response=True,
        #                       name="登录积分商城") as rsp:
        #     #获取请求数量
        #     #print(len(self.execNum))
        #     self.execNum.append(rsp.ok)
        #
        #     if "成功" in rsp.text:
        #         rsp.success()
        #     else:
        #         rsp.failure('selectStore 接口失败！')
        #
        #     self.stop(0, len(self.execNum))
        #     # current_time = time.time()
        #     # self.stop(current_time)
        req = requests.session().post(
            url="https://tapi.lifeat.cn:45788/user/login/login",
            json=datas,
            headers=self.headers
        )
        return req.json()

    @task
    def point_rule_list(self):
        datas = {"pageNum":1,"pageSize":10}
        self.headers["token"] = self.req["data"]["token"]
        with self.client.post(url="/points-cms/point-rule/list",
                              json=datas,
                              headers=self.headers,
                              catch_response=True,
                              name="积分规则列表") as rsp:


            if "成功" in rsp.text:
                rsp.success()
            else:
                rsp.failure('point_rule_list 接口失败！')


    @task
    def prize_list(self):
        datas ={"pageNum":1,"pageSize":10,"searchContent":""}
        self.headers["token"] = self.req["data"]["token"]
        with self.client.post(url="/marketing/cms/prize/page",
                              json=datas,
                              headers=self.headers,
                              catch_response=True,
                              name="奖品管理") as rsp:


            if "成功" in rsp.text:
                rsp.success()
            else:
                rsp.failure('prize_list 接口失败！')


    @task
    def prize_save(self):
        uploads=self.uploadqiniunp("C:/Users/vivid/Desktop/bug/","xingzhan.jpg")
        datas = {"category":"0",
                 "name":"hh1",
                 "img":"https://kfcdn.lifeat.cn/"+uploads["key"],
                 "explainInfo":"1234",
                 "getRuleExplain":"1234"}
        self.headers["token"] = self.req["data"]["token"]
        with self.client.post(url="/marketing/cms/prize/save",
                              json=datas,
                              headers=self.headers,
                              catch_response=True,
                              name="新增奖品") as rsp:
            # 获取请求数量
            # print(len(self.execNum))
            self.execNum.append(rsp.ok)

            if "成功" in rsp.text:
                rsp.success()
            else:
                rsp.failure('prize_list 接口失败！')
        self.stop(0, len(self.execNum))



    def uploadqiniunp(self,img_path,img_name, img_type='image/jpeg'):
        datas = {}
        self.headers["token"] = self.req["data"]["token"]
        upload = requests.session().post(
            url="https://tapi.lifeat.cn:45788/checkin/upload/uploadToken",
            json=datas,
            headers=self.headers
        )
        requests.session().get(
            url="https://api.qiniu.com/v2/query?ak=m1qdTqGcH54NLtQrE2j0MRnvKf8LaJBu1A7omyfe&bucket=easylife",
            headers=self.headers
        )
        loadToken = upload.json()
        print(loadToken)
        time.sleep(0.2)
        boundary = uuid.uuid4().hex
        self.headers["Content-Type"] = "multipart/form-data; boundary=----WebKitFormBoundary%s"%boundary[0:16]
        chioce_times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file = open(img_path + img_name, 'rb')
        files = {
            "token": (None, loadToken["data"]["imgToken"]),
            "fname": (img_name, file, img_type),
            "key": (None, chioce_times + ".jpg")
        }
        response = requests.session().post(
            url="https://upload-z1.qiniup.com/",
            files=files
        )
        time.sleep(1)
        return response.json()











class Locust_Test(HttpUser):
    tasks = [MarkerUser]
    wait_time = between(0.5, 3)



if __name__ == '__main__':
    os.system("locust -f s5.py --web-host=127.0.0.1")


