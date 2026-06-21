Feature: Login

Scenario: Successful Login

Given user opens login page

When user enters username "tomsmith"

And user enters password "SuperSecretPassword!"

And clicks Login

Then secure area should be displayed

And success message should appear