import unittest
import sys
import os

# Get the absolute path of the parent directory
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_directory)


from flask import Flask
from flask_testing import TestCase
sys.path.append('..')
from app import *

class TestApp(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        # Perform any setup steps if needed
        pass

    def tearDown(self):
        # Perform any cleanup steps if needed
        pass

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Deutsch/uebersicht.html')

    def test_overview(self):
        response = self.client.get('/overview')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Englisch/overview.html')

    def test_heute(self):
        response = self.client.get('/heute')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Deutsch/heute.html')

    def test_today(self):
        response = self.client.get('/today')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Englisch/today.html')

    def test_woche(self):
        response = self.client.get('/woche')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Deutsch/kalenderwoche.html')

    def test_week(self):
        response = self.client.get('/week')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Englisch/week.html')

    def test_monat(self):
        response = self.client.get('/monat')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Deutsch/monat.html')

    def test_month(self):
        response = self.client.get('/month')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Englisch/month.html')

    def test_administration(self):
        response = self.client.get('/administration')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Deutsch/admin.html')

    def test_admin(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('Englisch/settings.html')

    #def test_get_chart_data(self):

    def test_calculate_average(self):
        volume_values = [70, 80, 90, 100]
        label_values = [1,2,3,4]
        self.assertTrue(calculate_average(volume_values,label_values), ([1,2,3,4],[70,80,90,100]))

        volume_values = [70, 80, 90, 100]
        label_values = [1,2,1,2]
        self.assertTrue(calculate_average(volume_values,label_values), ([1,2],[80,90]))

        volume_values = [100,200,300]
        label_values = [1,2]
        assert calculate_average(volume_values,label_values) is None

        volume_values = []
        label_values = []
        assert calculate_average(volume_values,label_values) is None



if __name__ == '__main__':
    unittest.main()
