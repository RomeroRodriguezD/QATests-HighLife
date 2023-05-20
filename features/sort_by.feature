Feature: Sort By

  # Unit test

  Scenario: Landing on page for the first time
    When I check the default sorting option
    Then "Position" is selected as the default sorting option

  # Unit test

  Scenario: Checking sorting options available
    When I click with my mouse the "sort by" dropdown control
    Then I can see there are 4 options: Position, product name, price and new arrivals

  # Unit test

  Scenario: Price sort
    When I select "Price" option as sorting filter and the arrow icon remains untouched
    Then Products on that page should be sorted from lowest to highest price

  # Unit test

  Scenario: Name sort
    When I select "Product Name" option as sorting filter and the arrow icon remains untouched
    Then Products on that page should be sorted alphabetically

  # Unit test

  Scenario: New arrivals
    When I select "New Arrivals" option as sorting filter and the arrow icon remains untouched
    Then Products on that page should be sorted accordingly

  # Integration test

  Scenario: Price sort integrated on each page
    Given I have selected "Price" as sorting option
    When I save the prices and click on next page
    Then the sorting option is still applied and gives coherent order

  # Integration test

  Scenario: Product Name sort integrated on next page
    Given I have selected "Product Name" as sorting option
    When I click on next page
    Then the sorting option is still applied

  # Unit test

  Scenario Outline: Changing sorting option on the same page
    When I select "<sort_by_option>"
    Then the product order changes

        Examples:
          | sort_by_option |
          |  Price         |
          |  Product Name  |
          |  New Arrivals  |

  # Integration test

  Scenario Outline: Arrow sorting behaviour
    When I sort the list by "<sort_by_option>"
    And I click on the arrow up ↑ icon
    Then the product list order is reversed

    Examples:
          | sort_by_option |
          |  Price         |
          |  Product Name  |
          |  New Arrivals  |