*** Settings ***
Library    Browser

*** Variables ***
${LOGIN_URL}    https://the-internet.herokuapp.com/login
${USERNAME}    tomsmith
${PASSWORD}    SuperSecretPassword!

*** Keywords ***
Open Login Page
    New Page    ${LOGIN_URL}

Enter Username
    [Arguments]    ${username}
    Fill Text    id=username    ${username}

Enter Password
    [Arguments]    ${password}
    Fill Text    id=password    ${password}

Click Login Button
    Click    button[type='submit']

Verify Login Success
    Wait For Elements State    id=flash    visible
    Get Text    id=flash    contains    You logged into a secure area!

*** Test Cases ***
Login With Valid Credentials
    Open Login Page
    Enter Username    ${USERNAME}
    Enter Password    ${PASSWORD}
    Click Login Button
    Verify Login Success