*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${url}    https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}    chrome

*** Test Cases ***
LoginSuccessTest
    Open Browser    ${url}    ${browser}
    LoginValidCredential
    Click Button    xpath://*[@type='submit']
    Close Browser

LoginFailTest
    Open Browser    ${url}    ${browser}
    LoginInvalidCredential
    Click Button    xpath://*[@type='submit']
    Close Browser

*** Keywords ***
LoginValidCredential
    Wait Until Element Is Visible    name = username    10s
    Input Text    name = username    Admin
    Wait Until Element Is Visible    name = password    10s
    Input Text    name = password    admin123

LoginInvalidCredential
    Wait Until Element Is Visible    name = username    10s
    Input Text    name = username    Mohak
    Wait Until Element Is Visible    name = password    10s
    Input Text    name = password    mohak123