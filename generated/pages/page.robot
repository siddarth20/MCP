*** Variables ***
${LOGIN_URL}    https://the-internet.herokuapp.com/login
${SECURE_URL}    https://the-internet.herokuapp.com/secure
${USERNAME}    tomsmith
${PASSWORD}    SuperSecretPassword!
${SUCCESS_MESSAGE}    You logged into a secure area!

*** Keywords ***
Open Login Page
    New Browser    headless=${False}
    New Page    ${LOGIN_URL}

Enter Username
    [Arguments]    ${username}
    Fill Text    label=Username    ${username}

Enter Password
    [Arguments]    ${password}
    Fill Text    label=Password    ${password}

Click Login Button
    Click    text=Login

Verify Secure Page
    Get Url    ==    ${SECURE_URL}
    Get Text    text=${SUCCESS_MESSAGE}