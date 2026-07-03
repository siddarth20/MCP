*** Settings ***
Resource    LoginPage.robot

*** Test Cases ***
Valid Login
    Given user opens login page
    When user enters valid credentials
    Then login succeeds