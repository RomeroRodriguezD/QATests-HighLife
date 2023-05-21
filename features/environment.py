from behave import *
from support.fixtures import TestMethods

"""This code sets the main '@Given' for each test step, which includes running a webdriver with our
   landing page.
"""

def before_scenario(context, scenario):
    """Sets up a browser for each test, before its respective steps"""
    context.test_fixtures = TestMethods()
    use_fixture(context.test_fixtures.selenium_browser_firefox, context)

