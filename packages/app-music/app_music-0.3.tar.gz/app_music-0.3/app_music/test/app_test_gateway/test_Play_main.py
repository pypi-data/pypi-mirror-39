#! usr/bin/env python
# coding = utf-8

import unittest
from test.app_test_gateway.common import CommonSearch


class music(CommonSearch, unittest.TestCase):
    def test_music_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[4]['music']['url']
        body = self.searchlist[4]['music']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_music_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[4]['music']['url']
        body = self.searchlist[4]['music']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_music_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[4]['music']['url']
        body = self.searchlist[4]['music']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class play(CommonSearch, unittest.TestCase):
    def test_play_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[4]['play']['url']
        body = self.searchlist[4]['play']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_play_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[4]['play']['url']
        body = self.searchlist[4]['play']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_play_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[4]['play']['url']
        body = self.searchlist[4]['play']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


if __name__ == "__main__":
    unittest.main()
