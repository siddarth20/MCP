*** Settings ***
Documentation    Common keywords and setup
Library          Browser
Resource         config.robot

*** Keywords ***
Open Application
    [Documentation]    Opens the browser and sets common configurations
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Context    viewport={'width': 1920, 'height': 1080}
    Set Browser Timeout    ${TIMEOUT}