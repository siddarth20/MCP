*** Settings ***
Documentation    Page object for secure area
Library          Browser
Resource         ../common.robot

*** Variables ***
${SECURE_PAGE_URL}    /secure
${LOGOUT_BUTTON}      a.button.secondary.radius

*** Keywords ***
Verify Secure Page Loaded
    [Documentation]    Verifies the secure page is loaded
    Get Url    ==    ${BASE_URL}${SECURE_PAGE_URL}

Click Logout Button
    [Documentation]    Clicks the logout button
    Click    ${LOGOUT_BUTTON}