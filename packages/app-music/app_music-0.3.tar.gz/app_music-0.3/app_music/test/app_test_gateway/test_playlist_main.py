#! usr/bin/env python
# coding = utf-8

import unittest
from test.app_test_gateway.common import CommonSearch


class getplaylistcontent(CommonSearch, unittest.TestCase):
    def test_getplaylistcontent_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['getplaylistcontent']['url']
        body = self.searchlist[2]['getplaylistcontent']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_getplaylistcontent_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['getplaylistcontent']['url']
        body = self.searchlist[2]['getplaylistcontent']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_getplaylistcontent_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['getplaylistcontent']['url']
        body = self.searchlist[2]['getplaylistcontent']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class add(CommonSearch, unittest.TestCase):
    def test_add_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['add']['url']
        body = self.searchlist[2]['add']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_add_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['add']['url']
        body = self.searchlist[2]['add']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_add_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['add']['url']
        body = self.searchlist[2]['add']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_add_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['add']['url']
        body = self.searchlist[2]['add']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_add_5(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['add']['url']
        body = self.searchlist[2]['add']['body'][4]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_add_6(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['add']['url']
        body = self.searchlist[2]['add']['body'][5]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class delete(CommonSearch, unittest.TestCase):
    def test_delete_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['delete']['url']
        body = self.searchlist[2]['delete']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_delete_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['delete']['url']
        body = self.searchlist[2]['delete']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_delete_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['delete']['url']
        body = self.searchlist[2]['delete']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_delete_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['delete']['url']
        body = self.searchlist[2]['delete']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_delete_5(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['delete']['url']
        body = self.searchlist[2]['delete']['body'][4]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31006)  # 两个数字不相等，就False

    def test_delete_6(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['delete']['url']
        body = self.searchlist[2]['delete']['body'][5]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class create(CommonSearch, unittest.TestCase):
    def test_create_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['create']['url']
        body = self.searchlist[2]['create']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_create_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['create']['url']
        body = self.searchlist[2]['create']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31012)  # 两个数字不相等，就False

    def test_create_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[2]['create']['url']
        body = self.searchlist[2]['create']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


if __name__ == "__main__":
    unittest.main()
