*** Settings ***
Documentation    Page object for login page
Library          Browser
Resource         ../common.robot

*** Variables ***
${USERNAME_FIELD}        input[name="username"]
${PASSWORD_FIELD}        input[name="password"]
${LOGIN_BUTTON}          button[type="submit"]
${LOGIN_PAGE_URL}        /login

*** Keywords ***
Navigate To Login Page
    [Documentation]    Navigates to the login page
    Go To    ${BASE_URL}${LOGIN_PAGE_URL}

Enter Username
    [Arguments]    ${username}
    [Documentation]    Enters the username
    Fill Text    ${USERNAME_FIELD}    ${username}

Enter Password
    [Arguments]    ${password}
    [Documentation]    Enters the password
    Fill Text    ${PASSWORD_FIELD}    ${password}

Click Login Button
    [Documentation]    Clicks the login button
    Click    ${LOGIN_BUTTON}