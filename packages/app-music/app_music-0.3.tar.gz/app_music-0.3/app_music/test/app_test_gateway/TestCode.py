#! usr/bin/env python
# coding = utf-8


import requests


class UnitTestMain(object):
    def __init__(self):
        self.err_no = 0

    def get_start(self):
        return self.err_no

    def response_code(self, ip, url, headers, body):
        api_url = ip + url
        res = requests.post(url=api_url, json=eval(body), headers=headers).json()
        self.err_no = int(res['err_resp']['code'])

    # def music_search_code(self, ip, url, headers, body):
    #     api_url = ip + url
    #     res = requests.post(url=api_url, json=eval(body), headers=headers).json()
    #     self.err_no = int(res['err_resp']['code'])
    #
    # def artist_search_code(self, ip, url, headers, body):
    #     api_url = ip + url
    #     res = requests.post(url=api_url, json=eval(body), headers=headers).json()
    #     self.err_no = int(res['err_resp']['code'])
    #
    # def album_search_code(self, ip, url, headers, body):
    #     api_url = ip + url
    #     res = requests.post(url=api_url, json=eval(body), headers=headers).json()
    #     self.err_no = int(res['err_resp']['code'])
    #
    # def list_search_code(self, ip, url, headers, body):
    #     api_url = ip + url
    #     res = requests.post(url=api_url, json=eval(body), headers=headers).json()
    #     self.err_no = int(res['err_resp']['code'])
    #
    # def combine_search_code(self, ip, url, headers, body):
    #     api_url = ip + url
    #     res = requests.post(url=api_url, json=eval(body), headers=headers).json()
    #     self.err_no = int(res['err_resp']['code'])

    def dispose(self):
        pass
