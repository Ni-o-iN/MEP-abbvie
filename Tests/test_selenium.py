import unittest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import sys
import os
# Get the absolute path of the parent directory
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_directory)
import app
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Specify the path to the Microsoft Edge WebDriver executable
        edge_driver_path = '/path/to/edge/webdriver/executable'

        # Start the Flask app using a subprocess
        self.flask_process = subprocess.Popen(['python', 'app.py'])

        # Wait for the Flask app to start up (adjust the delay if needed)
        time.sleep(2)

        # Create a new instance of the Microsoft Edge WebDriver
        self.driver = webdriver.Edge(service=Service(edge_driver_path))
        self.driver.implicitly_wait(5)  # Wait for elements to load

    def tearDown(self):
        # Quit the WebDriver and terminate the Flask app process
        self.driver.quit()
        self.flask_process.terminate()
        print("tearDown complete")

    # def test_index(self):
    #     # Open the home page
    #     self.driver.get('http://localhost:5000')

    #     # Assert that the page title is correct !!WE NEED TITLES!!
    #     # self.assertEqual(self.driver.title, 'Your App | Home')

    #     # Assert that the expected content is present on the page
    #     welcome_text = self.driver.find_element_by_id('welcome').text
    #     self.assertEqual(welcome_text, 'Welcome to Your App')

    # def test_overview(self):
    #     # Open the overview page
    #     self.driver.get('http://localhost:5000/overview')

    #     # Assert that the page title is correct
    #     self.assertEqual(self.driver.title, 'Your App | Overview')

    #     # Assert that the expected content is present on the page
    #     heading_text = self.driver.find_element_by_css_selector('h1').text
    #     self.assertEqual(heading_text, 'Overview')

    #     # Assert that a specific element is present on the page
    #     self.assertTrue(self.driver.find_element_by_id('chart'))

##language-switch-tests##
    def prepare_test(self, url):
        self.driver.get(url)
        ActionChains(self.driver).move_to_element(self.driver.find_element(By.CLASS_NAME, "language-container")).perform()

    def click_element_by_id(self, element_id):
        self.driver.find_element("id", element_id).click()

    def is_same_url(self, url):
        return(self.driver.current_url == url)
    
    def test_uebersicht_to_overview(self):
        self.prepare_test('http://localhost:5000')
        self.click_element_by_id("english_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/overview'))

    def test_overview_to_uebersicht(self):
        self.prepare_test('http://localhost:5000/overview')
        self.click_element_by_id('german_page')
        self.assertTrue(self.is_same_url('http://localhost:5000'))

    def test_heute_to_today(self):
        self.prepare_test('http://localhost:5000/heute')
        self.click_element_by_id("english_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/today'))

    def test_heute_to_today(self):
        self.prepare_test('http://localhost:5000/today')
        self.click_element_by_id("german_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/heute'))

    def test_woche_to_week(self):
        self.prepare_test('http://localhost:5000/woche')
        self.click_element_by_id("english_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/week'))

    def test_week_to_woche(self):
        self.prepare_test('http://localhost:5000/week')
        self.click_element_by_id("german_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/woche'))

    def test_monat_to_month(self):
        self.prepare_test('http://localhost:5000/monat')
        self.click_element_by_id("english_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/month'))

    def test_month_to_monat(self):
        self.prepare_test('http://localhost:5000/month')
        self.click_element_by_id("german_page")
        self.assertTrue(self.is_same_url('http://localhost:5000/monat'))

    ## admin pages later on.

    def test_monat_area_clickable(self):
        self.driver.get('http://localhost:5000/monat')

        secondDropdown_element = self.driver.find_element("id", "secondDropdown")
        is_disabled = not secondDropdown_element.is_enabled()

        assert is_disabled

        first_dropdown = Select(self.driver.find_element("id", "firstDropdown"))

        # Select an option by value
        first_dropdown.select_by_value("floor1")

        assert secondDropdown_element.is_enabled()
    
if __name__ == '__main__':
    #unittest.main(argv=[''], defaultTest='AppTestCase.test_overview_to_uebersicht')
    unittest.main()
