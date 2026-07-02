*** Settings ***
Resource    ../resources/locators.resource
Resource    ../resources/common.resource

*** Variables ***
${LOGIN_URL}    https://the-internet.herokuapp.com/login
${EXPECTED_TITLE}    The Internet

*** Keywords ***
Open Login Page
    Navigate To    ${LOGIN_URL}
    Wait Until Page Contains    Login Page

Enter Valid Credentials
    Input Text    ${USERNAME_FIELD}    tomsmith
    Input Text    ${PASSWORD_FIELD}    SuperSecretPassword!
    Click Button    ${LOGIN_BUTTON}

Verify Login Successful
    Wait Until Page Contains    Secure Area
    Page Should Contain    You logged into a secure area!