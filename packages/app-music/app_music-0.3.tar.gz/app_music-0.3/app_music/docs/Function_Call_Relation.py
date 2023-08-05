#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： Function_Call_Relation.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018/7/23 10:03
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------


import requests
import json


def headers_localhost(requests_path):
    ip = "127.0.0.1"
    port = "8886"
    vin = "LSJA1234567890118"
    uid = "123456"
    urlstring = ["http://", ip, ":", port, requests_path]
    url = "".join(urlstring)
    headers = {"Vin": vin, "User_id": uid}
    return url, headers


def headers_map_47_100_220_189(requests_path):
    ip = "47.100.220.189"
    port = "8886"
    vin = "LSJA1234567890118"
    uid = "123456"
    urlstring = ["http://", ip, ":", port, requests_path]
    url = "".join(urlstring)
    headers = {"Vin": vin, "User_id": uid}
    return url, headers


def headers_47_100_220_189(requests_path):
    ip = "47.100.220.189"
    port = "8080/app-ris"
    token = "4BA251C3E0D25FFACA070E3F4C4A55CF83D15C01E6CD54E531D4FB8D80C35F0F"
    device_token = "2E56D70FF8B868E58268833FBBAFD35FE4DF5FBC349D8008595D8D69AFCEA5A6"
    content_type = "application/json;charset=UTF-8"
    urlstring = ["http://", ip, ":", port, requests_path]
    url = "".join(urlstring)
    headers = {"token": token, "device_token": device_token, "Content-Type": content_type}
    return url, headers


# # poisearch
# def poisearchf(requests_path):
#     url, headers = headers_localhost(requests_path)
#     content = {"keywords": "上", "page": "1", "timestamp": 1515377061.875, "location": "121.1928650000,31.2794500000"}
#     requests.post(url, data=json.dumps(content), headers=headers)
#
#
# # 追踪代码
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
# from app import search
# from app.search import *
#
# if __name__ == '__main__':
#     graphviz = GraphvizOutput()
#     graphviz.output_file = 'poisearch.png'
#     with PyCallGraph(output=graphviz):
#         # params = {'keywords': '上', 'page': '1', 'timestamp': 1532314668.3454516,
#         #           'location': '121.1928650000,31.2794500000',
#         #           'vin': 'LSJA1234567890118', 'uid': '123456', 'ip': '127.0.0.1'}
#         # search.poisearch(params)
#         poisearchf("/map/search/poisearch")
#         print("success!")

