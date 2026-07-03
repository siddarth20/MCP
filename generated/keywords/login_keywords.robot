*** Settings ***
Library    SeleniumLibrary
Library    ../pages/login_page.py
Library    ../pages/secure_area_page.py
Resource    ../config.py

*** Keywords ***
Open Login Page
    ${login_page}=    LoginPage    ${driver}
    ${login_page}=    Call Method    ${login_page}    load
    [Return]    ${login_page}

Enter Valid Credentials
    [Arguments]    ${login_page}
    ${login_page}=    Call Method    ${login_page}    enter_credentials    ${USERNAME}    ${PASSWORD}
    [Return]    ${login_page}

Submit Login Form
    [Arguments]    ${login_page}
    ${secure_area_page}=    Call Method    ${login_page}    submit
    [Return]    ${secure_area_page}

Verify Login Success
    [Arguments]    ${secure_area_page}
    ${secure_area_page}=    Call Method    ${secure_area_page}    is_loaded
    ${flash_message}=    Call Method    ${secure_area_page}    get_flash_message
    Should Contain    ${flash_message}    You logged into a secure area!
    [Return]    ${secure_area_page}