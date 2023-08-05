#! usr/bin/env python
# coding = utf-8

import unittest
from test.app_test_gateway.common import CommonSearch


class ArtistInfo(CommonSearch, unittest.TestCase):
    def test_artist_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['artistinfo']['url']
        body = self.searchlist[1]['artistinfo']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_artist_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['artistinfo']['url']
        body = self.searchlist[1]['artistinfo']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31014)  # 两个数字不相等，就False

    def test_artist_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['artistinfo']['url']
        body = self.searchlist[1]['artistinfo']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class AlbumInfo(CommonSearch, unittest.TestCase):
    def test_album_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['albuminfo']['url']
        body = self.searchlist[1]['albuminfo']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_album_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['albuminfo']['url']
        body = self.searchlist[1]['albuminfo']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31007)  # 两个数字不相等，就False

    def test_album_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['albuminfo']['url']
        body = self.searchlist[1]['albuminfo']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class ListInfo(CommonSearch, unittest.TestCase):
    def test_list_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['listinfo']['url']
        body = self.searchlist[1]['listinfo']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_list_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['listinfo']['url']
        body = self.searchlist[1]['listinfo']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31015)  # 两个数字不相等，就False

    def test_list_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['listinfo']['url']
        body = self.searchlist[1]['listinfo']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class Lyric(CommonSearch, unittest.TestCase):
    def test_lyric_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['lyric']['url']
        body = self.searchlist[1]['lyric']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_lyric_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['lyric']['url']
        body = self.searchlist[1]['lyric']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31011)  # 两个数字不相等，就False

    def test_alyric_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[1]['lyric']['url']
        body = self.searchlist[1]['lyric']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


if __name__ == "__main__":
    unittest.main()
