*** Settings ***
Resource    LoginPage.robot
Resource    config.robot
Resource    common_keywords.robot

*** Test Cases ***
Login Test Suite
    Open Browser With Config
    Login With Valid Credentials
    Close Browser Session