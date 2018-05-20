Feature: Open the Wikipedia webpage and perform a search

  @WIKIPEDIA
  Scenario Outline: My first Slayer test
    Given I open a browser
    And I navigate to the Wikipedia page
    When I search for the text '<search_query>'
    Then I see in the page '<search_result>'
  Examples:
    | search_query                | search_result                 |
    | Python language             | Python (programming language) |
    | Behavior Driven Development | Behavior-driven development   |
