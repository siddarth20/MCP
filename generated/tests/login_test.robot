*** Settings ***
Library    SeleniumLibrary
Resource    ../keywords/login_keywords.robot

*** Test Cases ***
Successful Login
    ${login_page}=    Open Login Page
    ${login_page}=    Enter Valid Credentials    ${login_page}
    ${secure_area_page}=    Submit Login Form    ${login_page}
    ${secure_area_page}=    Verify Login Success    ${secure_area_page}