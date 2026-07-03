*** Settings ***
Library    Browser

*** Keywords ***
Open Browser With Config
    New Browser    ${BROWSER}    headless=${HEADLESS}
    Set Browser Timeout    ${TIMEOUT}

Close Browser Session
    Close Browser