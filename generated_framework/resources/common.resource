*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Navigate To
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}
    Maximize Browser Window

Wait Until Page Contains
    [Arguments]    ${text}
    SeleniumLibrary.Wait Until Page Contains    ${text}    timeout=10s

Close All Browsers
    SeleniumLibrary.Close All Browsers