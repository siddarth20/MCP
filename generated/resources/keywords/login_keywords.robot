*** Settings ***
Documentation    Reusable login keywords
Library          Browser
Resource         ../common.robot
Resource         ../pages/login_page.robot
Resource         ../pages/secure_page.robot

*** Keywords ***
Login With Valid Credentials
    [Documentation]    Performs login with valid credentials
    Navigate To Login Page
    Enter Username    tomsmith
    Enter Password    SuperSecretPassword!
    Click Login Button
    Verify Secure Page Loaded