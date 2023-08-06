*** Settings ***
Documentation  Actions sur un PDF visionné depuis Firefox.

*** Keywords ***
Open PDF
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    [Arguments]  ${window}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Select Window  ${window}.php
    La page ne doit pas contenir d'erreur

Close PDF
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    Close Window
    Select Window

Previous Page PDF
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=#previous

Next Page PDF
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=#next

PDF Page Number Should Contain
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    [Arguments]  ${page_number}  ${text}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  css=#pageContainer${page_number}  ${text}

PDF Page Number Should Not Contain
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    [Arguments]  ${page_number}  ${text}
    Element Should Not Contain  css=#pageContainer${page_number}  ${text}

PDF Pages Number Should Be
    [Tags]
    [Documentation]  Spécifique à la visionneuse de firefox
    [Arguments]  ${total}
    ${over} =  Convert to Integer  ${total}
    ${over} =  Evaluate  ${over}+1
    Page Should Contain Element  css=#pageContainer${total}
    Page Should Not Contain Element  css=#pageContainer${over}
