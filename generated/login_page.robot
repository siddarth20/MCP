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
    Type Text    input[name='username']    ${USERNAME}

Enter Password
    Type Text    input[name='password']    ${PASSWORD}

Click Login Button
    Click    button[type='submit']

*** Test Cases ***
Login With Valid Credentials
    Open Login Page
    Enter Username
    Enter Password
    Click Login Button
    Wait For Elements    text=Welcome to the Secure Area