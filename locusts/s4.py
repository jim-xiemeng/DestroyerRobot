#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/16 13:09
# @Author : vivid
# @FileName: s4.py
# @Software: PyCharm
import time
from locust import HttpUser, task, between,TaskSet,tag
import requests

class MyTaskSet(TaskSet):
    def on_start(self):
        """
        初始化设置头信息
        :return:
        """
        self.headers =  {
            'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTU3MTg4Njg0NzgiLCJpYXQiOjE2MDkyMjc4NzIsImV4cCI6MTYwOTIzNTA3MiwibmJmIjoxNjA5MjI3ODcyfQ.j5NBSRBASJR9cQt_Qy2YD0iIxmixDn_ORicz4pud42o',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.pms_login = self.uat_login()


    @task
    def getUserInfo(self):
        getUserInfo = {
            "id": "611"
        }
        self.headers["token"]=self.pms_login["data"]["token"]
        self.headers["Authorization"]="Bearer" + " "+ self.pms_login["data"]["applicationToken"]
        # self.client.post(
        #     url="/user/api/getUserInfo",
        #     json=getUserInfo,
        #     headers=self.headers,
        #     catch_response=True
        # )
        with self.client.post(url="/user/api/getUserInfo",
                              json=getUserInfo,
                              headers=self.headers,
                              catch_response=True,
                              name="进入测试环境") as rsp:
            #print("rsp.text:",rsp.json())
            # if rsp.status_code > 400:
            #     print(rsp.text)
            #     rsp.failure('regist_ 接口失败！')
            if "成功" in rsp.text:
                rsp.success()
            else:
                rsp.failure('getUserInfo 接口失败！')




    @task
    def getAll(self):
        cities_datas = {
            "cityid": "",
            "provinceid": "",
            "regionId": "",
            "pageSize": 10,
            "pageNum": 1
        }
        self.headers["token"] = self.pms_login["data"]["token"]
        self.headers["Authorization"] = "Bearer" + " " + self.pms_login["data"]["applicationToken"]

        # response = self.client.post(
        #     url="/city/sysCity/getAll",
        #     json=cities_datas,
        #     headers=self.headers
        #
        # )

        with self.client.post(url="/city/sysCity/getAll",
                              json=cities_datas,
                              headers=self.headers,
                              catch_response=True,
                              name="获取首页信息") as rsp:
            if "成功" in rsp.text:
                rsp.success()
            else:
                rsp.failure('getAll 接口失败！')

    @task
    def selectStore(self):
        datas = {
            "cityid": "",
            "customerName": "",
            "leaderNameOrLeaderPhone": "",
            "pageNum": 10,
            "pageSize": 1,
            "status": "",
            "storeName": ""
        }
        self.headers["token"] = self.pms_login["data"]["token"]
        self.headers["Authorization"] = "Bearer" + " " + self.pms_login["data"]["applicationToken"]

        # response = self.client.post(
        #     url="/city/sysCity/getAll",
        #     json=cities_datas,
        #     headers=self.headers
        #
        # )

        with self.client.post(url="/cms/stores/stores/selectStore",
                              json=datas,
                              headers=self.headers,
                              catch_response=True,
                              name="进入经纪门店") as rsp:
            if "成功" in rsp.text:
                rsp.success()
            else:
                rsp.failure('selectStore 接口失败！')











    def uat_login(self):
        """
        这是一个原生requests请求,用于获取“帕斯通”中的token,Authorization
        :return:
        """
        url = "https://uat-pms-sso.hopsontong.com:11013/api/login"
        datas = {
            "mobile": "18718750404",
            "appFlag": "easylife-cms-api-gateway",
            "afsSessionId": "WjFlCkIWDpHT9odN",
            "afsSig": "QuAncgq0hrmAVNX0",
            "afsToken": "FFFF0N00000000009184:1591688607383:0.9844042761792562",
            "afsScene": "nc_login",
            "password": "123456"
        }

        response=requests.session().post(
            url,
            json=datas,
            headers=self.headers
        )
        response.encoding = response.apparent_encoding #根据浏览器编码格式，解码
        #print(response.text)
        return response.json()

class Locust_Test(HttpUser):
    tasks = [MyTaskSet]
    wait_time = between(0.1, 3)
    min_wait = 1000
    max_wait = 3000
