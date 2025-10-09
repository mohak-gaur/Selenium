*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${url}    https://cosmiminer.in/ravi/login.html
${browser}    chrome

*** Test Cases ***
LoginSuccessTest
    Open Browser    ${url}    ${browser}
    LoginValidCredentials
    RememberLoginCredentials
    PressLoginButton
    Close Browser

LoginFailTest
    Open Browser    ${url}    ${browser}
    LoginInvalidCredentials
    RememberLoginCredentials
    PressLoginButton
    Close Browser

MiningStarted
    Open Browser    ${url}    ${browser}
    LoginValidCredentials
    RememberLoginCredentials
    PressLoginButton
    Sleep    1s
    ClosePopup
    Sleep    2s
    PressMiningButton
    Sleep    2s
    Close Browser

*** Keywords ***
LoginValidCredentials
    Wait Until Element Is Visible    name = email    10s
    Input Text    name = email    cosmic_miner_main@yopmail.com
    Wait Until Element Is Visible    name = password    10s
    Input Text    name = password    Admin123!

LoginInvalidCredentials
    Wait Until Element Is Visible    name = email    10s
    Input Text    name = email    admin@yopmail.com
    Element Should Be Visible    name = password    10s
    Input Password    name = password    admin123

PressLoginButton
    Element Should Be Visible    id = login-btn    10s
    Click Button    id = login-btn

RememberLoginCredentials
    Element Should Be Visible    id = remember    10s
    Click Button    id = remember

PressMiningButton
    Element Should Be Visible    xpath://button[@id='startMiningBtn']    10s
    Scroll Element Into View    xpath://button[@id='startMiningBtn']
    # ${startMining}=    Get WebElement    xpath://button[@id='startMiningBtn']
    # Execute JavaScript    arguments[0].scrollIntoView(true);    ${startMining}
    Click Button    id = startMiningBtn
    # Sleep    1s
    # Click Element    ${startMining}

ClosePopup
    Element Should Be Visible    id = closePopup    10s
    Click Button    id = closePopup