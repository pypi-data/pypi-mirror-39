#! usr/bin/env python
# coding = utf-8


# import os
import unittest
# from ruamel import yaml
# from test.app_test_gateway.unittest_code.SearchTestCode import UnitSearchMain
from test.app_test_gateway.common import CommonSearch


# def yamlPath():
#     path = os.getcwd() + '/app_test_gateway/yaml/data.yaml'
#     f = open(path, encoding='utf-8')
#     y = yaml.safe_load(f)
#     return y


class AssociateSearch(CommonSearch, unittest.TestCase):
    # def setUp(self):
    #     self.um = UnitSearchMain()
    #     y = yamlPath()
    #
    #     self.url = y['ip']
    #     self.associate_search = y['associate_search']
    #     self.headers = y['headers']
    #
    # def tearDown(self):
    #     self.um.dispose()
    #     self.um = None

    def test_associate_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['associate_search']['url']
        # headers = self.headers
        # headers = self.associate_search['headers']
        body = self.searchlist[0]['associate_search']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_associate_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['associate_search']['url']
        # headers = self.associate_search['headers']
        body = self.searchlist[0]['associate_search']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31003)  # 两个数字不相等，就False

    def test_associate_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['associate_search']['url']
        # headers = self.associate_search['headers']
        body = self.searchlist[0]['associate_search']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class MusicSearch(CommonSearch, unittest.TestCase):
    # def setUp(self):
    #     self.um = UnitSearchMain()
    #     y = yamlPath()
    #
    #     self.url = y['ip']
    #     self.music_search = y['music_search']
    #     self.headers = y['headers']
    #
    # def tearDown(self):
    #     self.um.dispose()
    #     self.um = None

    def test_music_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['music_search']['url']
        # headers = self.music_search['headers']
        body = self.searchlist[0]['music_search']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_music_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['music_search']['url']
        # headers = self.music_search['headers']
        body = self.searchlist[0]['music_search']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31003)  # 两个数字不相等，就False

    def test_music_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['music_search']['url']
        # headers = self.music_search['headers']
        body = self.searchlist[0]['music_search']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_music_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['music_search']['url']
        # headers = self.music_search['headers']
        body = self.searchlist[0]['music_search']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class ArtistSearch(CommonSearch, unittest.TestCase):
    # def setUp(self):
    #     self.um = UnitSearchMain()
    #     y = yamlPath()
    #
    #     self.url = y['ip']
    #     self.artist_search = y['artist_search']
    #     self.headers = y['headers']
    #
    # def tearDown(self):
    #     self.um.dispose()
    #     self.um = None

    def test_artist_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['artist_search']['url']
        # headers = self.artist_search['headers']
        body = self.searchlist[0]['artist_search']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_artist_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['artist_search']['url']
        # headers = self.artist_search['headers']
        body = self.searchlist[0]['artist_search']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31003)  # 两个数字不相等，就False

    def test_artist_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['artist_search']['url']
        # headers = self.artist_search['headers']
        body = self.searchlist[0]['artist_search']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_artist_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['artist_search']['url']
        # headers = self.artist_search['headers']
        body = self.searchlist[0]['artist_search']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class AlbumSearch(CommonSearch, unittest.TestCase):
    # def setUp(self):
    #     self.um = UnitSearchMain()
    #     y = yamlPath()
    #
    #     self.url = y['ip']
    #     self.album_search = y['album_search']
    #     self.headers = y['headers']
    #
    # def tearDown(self):
    #     self.um.dispose()
    #     self.um = None

    def test_album_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['album_search']['url']
        # headers = self.album_search['headers']
        body = self.searchlist[0]['album_search']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_album_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['album_search']['url']
        # headers = self.album_search['headers']
        body = self.searchlist[0]['album_search']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31003)  # 两个数字不相等，就False

    def test_album_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['album_search']['url']
        # headers = self.album_search['headers']
        body = self.searchlist[0]['album_search']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_album_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['album_search']['url']
        # headers = self.album_search['headers']
        body = self.searchlist[0]['album_search']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_album_5(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['album_search']['url']
        # headers = self.album_search['headers']
        body = self.searchlist[0]['album_search']['body'][4]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class ListSearch(CommonSearch, unittest.TestCase):
    # def setUp(self):
    #     self.um = UnitSearchMain()
    #     y = yamlPath()
    #
    #     self.url = y['ip']
    #     self.list_search = y['list_search']
    #     self.headers = y['headers']
    #
    # def tearDown(self):
    #     self.um.dispose()
    #     self.um = None

    def test_list_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['list_search']['url']
        # headers = self.list_search['headers']
        body = self.searchlist[0]['list_search']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_list_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['list_search']['url']
        # headers = self.list_search['headers']
        body = self.searchlist[0]['list_search']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31003)  # 两个数字不相等，就False

    def test_list_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['list_search']['url']
        # headers = self.list_search['headers']
        body = self.searchlist[0]['list_search']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


class CombineSearch(CommonSearch, unittest.TestCase):
    # def setUp(self):
    #     self.um = UnitSearchMain()
    #     y = yamlPath()
    #
    #     self.url = y['ip']
    #     self.combine_search = y['combine_search']
    #     self.headers = y['headers']
    #
    # def tearDown(self):
    #     self.um.dispose()
    #     self.um = None

    def test_combine_1(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['combine_search']['url']
        # headers = self.combine_search['headers']
        body = self.searchlist[0]['combine_search']['body'][0]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_combine_2(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['combine_search']['url']
        # headers = self.combine_search['headers']
        body = self.searchlist[0]['combine_search']['body'][1]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 31003)  # 两个数字不相等，就False

    def test_combine_3(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['combine_search']['url']
        # headers = self.combine_search['headers']
        body = self.searchlist[0]['combine_search']['body'][2]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_combine_4(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['combine_search']['url']
        # headers = self.combine_search['headers']
        body = self.searchlist[0]['combine_search']['body'][3]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False

    def test_combine_5(self):
        # 未输入 关键字
        ip = self.url
        url = self.searchlist[0]['combine_search']['url']
        # headers = self.combine_search['headers']
        body = self.searchlist[0]['combine_search']['body'][4]['body_']

        self.um.response_code(ip, url, self.headers, body)
        self.assertEqual(self.um.get_start(), 0)  # 两个数字不相等，就False


if __name__ == "__main__":
    unittest.main()
