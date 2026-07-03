from locators import *
from robot.api.deco import keyword

@keyword
def verify_login_page_loaded():
    return f"Should Be Visible    {LOGIN_PAGE_HEADER}"

@keyword
def input_username(username):
    return f"Fill Text    {USERNAME_FIELD}    {username}"

@keyword
def input_password(password):
    return f"Fill Text    {PASSWORD_FIELD}    {password}"

@keyword
def click_login_button():
    return f"Click    {LOGIN_BUTTON}"

@keyword
def verify_login_successful():
    return f"Should Be Visible    {SECURE_AREA_HEADER}"