Feature: Open Google


  @TAG_1
  Scenario: Open a web page
    Given I open a browser
    And I go to the Google web page

  @TAG_2 @WIP
  Scenario: Open yet another web page
    Given I open a browser
    And I go to the Google web page

  @TAG_3 @AUTORETRY
  Scenario: Open yet another web page 2
    Given I open a browser
    And I go to the Google web page
    And I wait for an invalid element

  @TAG_4
  Scenario: Test logging
    Given I test logging

  @TAG_5
  Scenario: My first Slayer test
    Given I open a browser
    Given I navigate to the Wikipedia page
    When I search for the text 'Behavior Driven Development'
    Then I see the page for 'Behavior-driven development'
