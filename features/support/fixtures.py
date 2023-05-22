from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import *
import requests
import random
from time import sleep

class TestMethods:
    @fixture
    def selenium_browser_firefox(self, context):
        """Sets up a browser for each test"""
        firefox_profile = webdriver.FirefoxProfile()
        options = webdriver.FirefoxOptions()
        firefox_profile.set_preference('webdriver.log.file', './log_file.log')  # Selenium register file
        context.browser = webdriver.Firefox(firefox_profile=firefox_profile, options=options)
        wait = WebDriverWait(context.browser, 10)
        try:
            url = 'https://highlifeshop.com/speedbird-cafe'
            context.browser.get(url)
            status_code = context.test_fixtures.get_response_code(context)
            assert status_code == 200
            context.browser.maximize_window()
            cookies = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/aside/div/form/div[2]/div[2]/button[1]')))
            cookies.click()
            sleep(3)

        except AssertionError:
            status_code = context.test_fixtures.get_response_code(context)
            raise AssertionError(f"Error: Unexpected response code. Expected 200, but got {status_code}.")

        yield context.browser
        context.browser.quit()

    @fixture
    def get_response_code(self, context):
        """Returns response code through requests, since Selenium can't do it on its own"""
        current_web = context.browser.current_url
        check_request = requests.get(current_web)
        status_code = check_request.status_code
        return status_code

    @fixture
    def check_default_sorting_option(self, context):
        """Checks which one is the selected option. First fetches the sorter element, then iterates through options to find
        the selected one and stores the value in a context variable."""
        sorting_list = context.browser.find_element(By.ID, 'sorter')
        context.selected_option = ""
        options = sorting_list.find_elements(By.TAG_NAME, 'option')
        for option in options:
            try:
                selected = option.get_attribute("selected")
                if selected is not None:
                    context.selected_option = option.text
            except:
                continue

    @fixture
    def scrolling(self, context):
        """Scroll down the page. It will do it the exact number of times needed, although down below
           we could see a generic approach to the scrolling feature.
        """
        iterations = 2
        window_height = context.browser.execute_script("return window.innerHeight")
        for scroll in range(iterations):
            context.browser.execute_script(f"window.scrollBy(0, {window_height});")
            sleep(random.uniform(1.5, 3.5))


        """Usually this would be the approach to scroll down to the page, regardless of its dimensions, but
           since we know exactly how many scrolls we need, we can set an specific number of iterations.
        """

        #window_height = context.browser.execute_script("return window.innerHeight")
        #height_count = window_height
        #last_height = context.browser.execute_script("return document.body.scrollHeight")

        #while True:
            #print('Window height: ', height_count, ' Document height: ', last_height)
            #context.browser.execute_script(f"window.scrollBy(0, {window_height});")
            #height_count += window_height
            #sleep(random.uniform(3, 5))
            #last_height = context.browser.execute_script("return document.body.scrollHeight")
            #if height_count >= last_height:
            #    context.browser.execute_script(f"window.scrollBy(0, -{window_height});")
            #    break
