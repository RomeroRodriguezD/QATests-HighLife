from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

""" Disclaimer: The code in features/environment.py sets up the main "Given" for each step, running a browser
   with the main page and accepting cookies, so we don't need to define neither a Given or a Background
   in Gherkin language for the majority of the cases.
"""

# First scenario: Landing on page for the first time

@when('I check the default sorting option')
def check_sorter(context):
    use_fixture(context.test_fixtures.check_default_sorting_option, context)

@then('"Position" is selected as the default sorting option')
def assert_position_as_default(context):
    assert context.selected_option == "Position"

# Second scenario: Checking sorting options available

@when('I click with my mouse the "sort by" dropdown control')
def check_sorting_options(context):

    sorting_list = context.browser.find_element(By.ID, 'sorter')
    sorting_options = sorting_list.find_elements(By.TAG_NAME, 'option')
    context.option_tags = [option.text for option in sorting_options]

@then('I can see there are 4 options: Position, product name, price and new arrivals')
def assert_options_amount(context):
    """Verifies if the dropdown menu has all the expected options"""
    expected_options = ["Position", "Price", "Product Name", "New Arrivals"]
    assert all(option in context.option_tags for option in expected_options)

# Third scenario: Price sort

@when('I select "Price" option as sorting filter and the arrow icon remains untouched')
def price_sort(context):
    """Sets Price as sorting option. We could also use just a modified URL
       as a request to the API using parameters: 'https://highlifeshop.com/speedbird-cafe?p=4&product_list_limit=30&product_list_order=price'.
    """
    sorter = context.browser.find_element(By.ID, 'sorter')
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text('Price')


@then('Products on that page should be sorted from lowest to highest price')
def assert_prices_are_sorted(context):
    """Checks if the prices on this page are sorted from lowest to highest. We'll give
       it a few seconds to load the page, just in case we have some net delay.
    """
    sleep(3)
    prices = context.browser.find_elements(By.CLASS_NAME, 'price')
    filtered_prices = []

    # Here we filter only the prices of products listed while ignoring the suggestions by setting a limit on the 18th index,
    # since each price appears twice: Pawn & AVIOS. We should get 9 prices sorted correctly, not more, not less.

    for item in prices[:18]:
        product_price = str(item.text)
        product_price = product_price.replace('£','')

        try:
            product_price = float(product_price)
        except:
            continue # This means we are handling a price in "AVIOS", which I'll refuse to only use pawns.

        print(product_price)
        filtered_prices.append(product_price)

    assert len(filtered_prices) == 9 # We should get 9 values, since that's how many products we are displaying by default

    sorted_prices = sorted(filtered_prices)  # Sorts the list of prices. It should match "filtered prices".

    assert filtered_prices == sorted_prices # Asserts the order of the prices is also the desired one (ascendant)

# Fourth scenario: Name sort

@when('I select "Product Name" option as sorting filter and the arrow icon remains untouched')
def product_name_sort(context):
    """Sets Product Name as sorting option
    """
    sorter = context.browser.find_element(By.ID, 'sorter')
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text('Product Name')

@then('Products on that page should be sorted alphabetically')
def assert_names_are_sorted(context):
    """Checks if the products are sorted alphabetically. This means they're supposed to start from A (or the closest letter
    to A) up to Z (or the last letter). Also, the total lenght of products fetched should be 9 (listed ones) + 4 (suggestions)
    """
    sleep(3)
    EXPECTED_LENGHT = 13

    product_names = context.browser.find_elements(By.CLASS_NAME, 'product-item-link')
    product_names = [product.text.replace(' ','') for product in product_names]
    product_names_clean = product_names[:9] # Product names without suggestions

    sorted_names = sorted(product_names_clean)

    assert len(product_names) == EXPECTED_LENGHT
    assert product_names_clean == sorted_names

    """This is supposed to fail, since first page sorted by name isn't perfectly sorted, first product starts with letter K, 
        and also only displays 8 items, instead of 9.
    """

# Fifth scenario: New Arrivals

@when('I select "New Arrivals" option as sorting filter and the arrow icon remains untouched')
def product_name_sort(context):
    """Sets new arrivals as sorting option
    """
    sorter = context.browser.find_element(By.ID, 'sorter')
    context.position_first = context.browser.find_element(By.CLASS_NAME, 'product-item-link').text
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text('New Arrivals')
    sleep(3)

@then('Products on that page should be sorted accordingly')
def assert_arrivals_are_sorted(context):
    """Maybe we don't know how we determine which products are new arrivals, but we can check
       if selecting this option, the order changed, by checking if the first item is the same or not.
    """
    context.arrival_first = context.browser.find_element(By.CLASS_NAME, 'product-item-link').text

    assert context.position_first != context.arrival_first

# Sixth scenario: Price sort integrated on each page

@given('I have selected "Price" as sorting option')
def price_sorting(context):
    sorter = context.browser.find_element(By.ID, 'sorter')
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text('Price')


@when('I save the prices and click on next page')
def next_page(context):
    """This function will iterate through pages and save all the prices
       for future comparison.
    """

    no_next_page = False
    context.filtered_prices = []
    while not no_next_page:
        try:
            use_fixture(context.test_fixtures.scrolling, context) # Scrolls down looking for next button
            sleep(3)
            prices = context.browser.find_elements(By.CLASS_NAME, 'price')

            for item in prices[:18]:
                product_price = str(item.text)
                product_price = product_price.replace('£', '')

                try:
                    product_price = float(product_price)
                    context.filtered_prices.append(product_price)
                except:
                    continue  # This means we are handling a price in "AVIOS", which I'll refuse to only use pawns.

            # Here it will try to find the next page button. If it is disabled, which should happen on last page, it will break the loop.
            next_button = context.browser.find_element(By.CSS_SELECTOR,
                                                       '#maincontent > div.columns > div.column.main > div:nth-child(7) > div.pages > ul > li.item.pages-item-next > a').click()
            sleep(4)

        except:
            no_next_page = True

@then('the sorting option is still applied and gives coherent order')
def check_sorting_results(context):
    """Checks if the prices are sorted correctly through pages.
       This test is supposed to fail since the price of "MEAL BUNDLE",
       product 95 when sorted by price, shows 2 prices instead of one,
       making the sorting comparison fail.
    """

    context.sorted_prices = sorted(context.filtered_prices)
    assert context.sorted_prices == context.filtered_prices # we check if our price sorting filter have worked through all the pages.

# Seventh scenario: Product Name sort integrated on each page

@given('I have selected "Product Name" as sorting option')
def name_sorting(context):
    sorter = context.browser.find_element(By.ID, 'sorter')
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text('Product Name')

@when('I click on next page')
def next_page(context):
    """
    For the sake of simplicity,this time it will only check if the sorting option
    remains up on the next page -also we already know it does not work correctly intentionally,
    since the first item sorted starts with letter "K"-.
    """
    use_fixture(context.test_fixtures.scrolling, context)  # Scrolls down looking for next button
    next_button = context.browser.find_element(By.CSS_SELECTOR,
                                               '#maincontent > div.columns > div.column.main > div:nth-child(7) > div.pages > ul > li.item.pages-item-next > a').click()
    sleep(4)

@then('the sorting option is still applied')
def name_sort_still_up(context):
    use_fixture(context.test_fixtures.check_default_sorting_option, context)

    assert context.selected_option == "Product Name"

# Eighth scenario: Changing sorting option on the same page

@when('I select "{sort_by_option}"')
def switch_option(context, sort_by_option):
    """We'll store the first item sorted by default, then we'll compare it with the ones sorted.
       If there's a new sorting order, it should have changed.
    """
    context.starting_product = context.browser.find_element(By.CLASS_NAME, 'product-item-link').text
    sorter = context.browser.find_element(By.ID, 'sorter')
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text(sort_by_option)

@then('the product order changes')
def check_product_change(context):
    context.new_sorted_product = context.browser.find_element(By.CLASS_NAME, 'product-item-link').text

    assert context.starting_product != context.new_sorted_product

# Nineth scenario: Arrow sorting behaviour

@when('I sort the list by "{sort_by_option}"')
def switch_option(context, sort_by_option):
    """
    Again, we'll store the first item sorted by default, then we'll compare it with the post-arrow change one.
    """
    sorter = context.browser.find_element(By.ID, 'sorter')
    sorting_select = Select(sorter)
    sorting_select.select_by_visible_text(sort_by_option)
    sleep(3)
    context.default_products_order = context.browser.find_elements(By.CLASS_NAME, 'product-item-link') # First we get all the products
    context.first_default_product = context.default_products_order[0].text
    context.last_default_product = context.default_products_order[8].text # I specify 8 and not -1, because I want to omit the suggestions

@when('I click on the arrow up ↑ icon')
def arrow_switch(context):
    arrow_button = context.browser.find_element(By.CSS_SELECTOR,
                                                '.sorter-action').click()
    sleep(3) # Give it time to change order
    context.new_default_order = context.browser.find_elements(By.CLASS_NAME, 'product-item-link')
    context.new_first_product = context.new_default_order[0].text
    context.new_last_product = context.new_default_order[8].text

@then('the product list order is reversed')
def assert_reversed_order(context):

    assert context.new_first_product != context.first_default_product
    assert context.new_last_product != context.last_default_product