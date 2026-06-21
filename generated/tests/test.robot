*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../pages/page.robot

*** Test Cases ***
Login Test
    [Documentation]    Verify successful login
    Given user opens login page
    When user enters valid credentials
    Then login succeeds