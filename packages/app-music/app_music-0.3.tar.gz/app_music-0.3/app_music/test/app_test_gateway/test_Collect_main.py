#! usr/bin/env python
# coding = utf-8

import unittest
from test.app_test_gateway.common import CommonSearch


class addsong(CommonSearch, unittest.TestCase):
    # def test_addsong_1(self):
    #     # 未输入 关键字
    #     ip = self.url
    #     url = self.searchlist[3]['addsong']['url']
    #     body = self.searchlist[3]['addsong']['body'][0]['body_']
    #
    #     self.um.response_code(ip, url, self.headers, body)
    #     self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_addsong_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['addsong']['url']
        body = self.searchlist[3]['addsong']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_addsong_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['addsong']['url']
        body = self.searchlist[3]['addsong']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class delsong(CommonSearch, unittest.TestCase):
    # def test_delsong_1(self):
    #     # 未输入 关键字
    #     ip = self.url
    #     url = self.searchlist[3]['delsong']['url']
    #     body = self.searchlist[3]['delsong']['body'][0]['body_']
    #
    #     self.um.response_code(ip, url, self.headers, body)
    #     self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_delsong_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['delsong']['url']
        body = self.searchlist[3]['delsong']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_delsong_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['delsong']['url']
        body = self.searchlist[3]['delsong']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class dellist(CommonSearch, unittest.TestCase):
    def test_dellist_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['dellist']['url']
        body = self.searchlist[3]['dellist']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_dellist_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['dellist']['url']
        body = self.searchlist[3]['dellist']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31013)  # 两个数字不相等，就False

    def test_dellist_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['dellist']['url']
        body = self.searchlist[3]['dellist']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31013)  # 两个数字不相等，就False

    def test_dellist_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['dellist']['url']
        body = self.searchlist[3]['dellist']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    # def test_dellist_5(self):
    #     # 未输入 关键字
    #     ip = self.url
    #     url = self.searchlist[3]['dellist']['url']
    #     body = self.searchlist[3]['dellist']['body'][4]['body_']
    #
    #     self.um.response_code(ip, url, self.headers, body)
    #     self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    # def test_dellist_6(self):
    #     # 未输入 关键字
    #     ip = self.url
    #     url = self.searchlist[3]['dellist']['url']
    #     body = self.searchlist[3]['dellist']['body'][5]['body_']
    #
    #     self.um.response_code(ip, url, self.headers, body)
    #     self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class addlist(CommonSearch, unittest.TestCase):
    def test_addlist_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['addlist']['url']
        body = self.searchlist[3]['addlist']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_addlist_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['addlist']['url']
        body = self.searchlist[3]['addlist']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31018)  # 两个数字不相等，就False

    def test_addlist_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['addlist']['url']
        body = self.searchlist[3]['addlist']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31018)  # 两个数字不相等，就False

    def test_addlist_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[3]['addlist']['url']
        body = self.searchlist[3]['addlist']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    # def test_addlist_5(self):
    #     # 未输入 关键字
    #     ip = self.url
    #     url = self.searchlist[3]['addlist']['url']
    #     body = self.searchlist[3]['addlist']['body'][4]['body_']
    #
    #     self.um.response_code(ip, url, self.headers, body)
    #     self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    # def test_addlist_6(self):
    #     # 未输入 关键字
    #     ip = self.url
    #     url = self.searchlist[3]['addlist']['url']
    #     body = self.searchlist[3]['addlist']['body'][5]['body_']
    #
    #     self.um.response_code(ip, url, self.headers, body)
    #     self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


if __name__ == "__main__":
    unittest.main()
