*** Settings ***
Resource    ../resources/common.resource
Resource    ../pages/login_page.resource

*** Test Cases ***
User Can Login With Valid Credentials
    Given user opens login page
    When user enters valid credentials
    Then login succeeds