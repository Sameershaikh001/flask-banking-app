Feature: Fund Transfer
  As a bank customer
  I want to transfer money to another user
  So that I can pay them

  Background:
    Given the following users exist:
      | username | email           | password | balance |
      | alice    | alice@test.com   | pass     | 500     |
      | bob      | bob@test.com     | pass     | 0       |

  Scenario: Successful transfer
    When Alice logs in
    And she transfers 100 to Bob
    Then Alice's balance should be 400
    And Bob's balance should be 100
    And a transaction record should exist between them