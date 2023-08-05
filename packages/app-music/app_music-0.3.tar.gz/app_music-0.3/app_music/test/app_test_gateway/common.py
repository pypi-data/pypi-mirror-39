#! usr/bin/env python
# coding = utf-8


import os
import unittest
from ruamel import yaml
from test.app_test_gateway.TestCode import UnitTestMain


def yamlPath():
    path = os.getcwd() + '/app_test_gateway/data.yaml'
    f = open(path, encoding='utf-8')
    y = yaml.safe_load(f)
    return y


class CommonSearch(unittest.TestCase):

    def setUp(self):
        self.um = UnitTestMain()
        y = yamlPath()

        self.url = y['ip']
        self.headers = y['headers']

        searchlist = []
        items = ['search', 'more', 'palylist', 'collect', 'play']
        for item in items:
            searchlist.append(y[item])
        self.searchlist = searchlist
        # print(searchlist)

    def tearDown(self):
        self.um.dispose()
        self.um = None
