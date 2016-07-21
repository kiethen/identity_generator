# -*- coding: utf-8 -*-

import unittest
import requests


class TestApi(unittest.TestCase):
    def setUp(self):
        self._url = 'http://127.0.0.1:5000/api'

    def test_api_by_sex_female(self):
        r = requests.get(self._url, params={'sex': 1})
        self.assertEqual(u'女', r.json()['sex'])

    def test_api_by_sex_male(self):
        r = requests.get(self._url, params={'sex': 2})
        self.assertEqual(u'男', r.json()['sex'])

    def test_api_by_year(self):
        r = requests.get(self._url, params={'year': 1988})
        self.assertEqual(u'1988', r.json()['birthday'][0:4])

    def test_api_by_month(self):
        r = requests.get(self._url, params={'month': 3})
        self.assertEqual(u'03', r.json()['birthday'][5:7])

    def test_api_by_day(self):
        r = requests.get(self._url, params={'day': 12})
        self.assertEqual(u'12', r.json()['birthday'][-2:])

if __name__ == '__main__':
    unittest.main()
