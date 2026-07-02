*** Settings ***
Resource    ../resources/locators.resource
Resource    ../resources/common.resource

*** Keywords ***
User Opens Login Page
    Open Login Page

User Enters Valid Credentials
    Enter Valid Credentials

Login Succeeds
    Verify Login Successful