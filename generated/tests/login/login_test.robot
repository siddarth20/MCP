*** Settings ***
Documentation    Login test cases
Library          Browser
Resource         ../../resources/common.robot
Resource         ../../resources/pages/login_page.robot

*** Test Cases ***
Successful Login
    [Documentation]    Verify user can login with valid credentials
    Open Application
    Navigate To Login Page
    Enter Username    tomsmith
    Enter Password    SuperSecretPassword!
    Click Login Button
    Get Url    ==    ${BASE_URL}/secure
    Close Browser