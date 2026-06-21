*** Keywords ***
User Opens Login Page
    Open Login Page

User Enters Valid Credentials
    Enter Username    ${USERNAME}
    Enter Password    ${PASSWORD}
    Click Login Button

Login Succeeds
    Verify Secure Page