*** Settings ***
Documentation     Actions dans un formulaire

*** Keywords ***
Click On Add Button
    [Tags]
    Click Element    css=span.add-16
    La page ne doit pas contenir d'erreur

Click On Add Button JS
    [Tags]
    [Arguments]    ${time}=1
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=span.add-16
    Sleep    ${time}
    La page ne doit pas contenir d'erreur

Click On Submit Button
    [Tags]
    [Arguments]    ${nomessage}=false  ${subform}=false
    # id du formulaire (selon si c'est un sous-formulaire ou non)
    ${form}=  Run Keyword If  '${subform}' != 'false'
    ...  Set Variable  sformulaire
    ...  ELSE  Set Variable  formulaire
    # définition du locator du bouton de validation, passé aux autres fonctions
    ${submitBtns}=  Set Variable  css=#${form} div.formControls input[type="submit"]
    # si on ne souhaite pas vérifier le message de validation, on clic simplement
    Run Keyword If  '${nomessage}' != 'false'  Click Element  ${submitBtns}
    # sinon on lance une boucle qui retente de cliquer tant qu'il n'a pas de
    # message de validation
    Run Keyword If  '${nomessage}' == 'false'  Click On Submit Button Until Validation Message  ${submitBtns}
    La page ne doit pas contenir d'erreur

Click On Submit Button Until Validation Message
    [Tags]
    [Arguments]    ${btn_locator}
    # 3 essais de clic sur le bouton de validation du formulaire (passé en paramètre)
    :FOR  ${INDEX}  IN RANGE  1  3
    \  # attente du succès du clic pendant 3 secondes max
    \  Wait Until Keyword Succeeds     3     ${RETRY_INTERVAL}    Click Element  ${btn_locator}
    \  # attente du message de validation pendant 5 secondes max
    \  ${status}=  Run Keyword And Return Status
    \  ...  Wait Until Keyword Succeeds  5  ${RETRY_INTERVAL}  Element Should Be Visible  css=div.message
    \  # si on a eu un message de validation, on sort de la boucle
    \  Exit For Loop If  ${status}

Click On Submit Button In Subform
    [Tags]
    Click On Submit Button  false  true

Click On Submit Button In Overlay
    [Tags]
    [Arguments]    ${obj}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element  css=#form-${obj}-overlay div.formControls input[type="submit"]
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On Back Button
    [Tags]
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=a.retour
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On Back Button In Subform
    [Tags]
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=#sformulaire a.retour
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On Back Button In Overlay
    [Tags]
    [Arguments]    ${obj}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=#form-${obj}-overlay form a.retour
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On Form Tab
    [Tags]
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Link      main
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On Httpclick Element
    [Tags]
    [Documentation]    Clique sur un champ de type httpclick.
    [Arguments]    ${element_id}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=.field-type-httpclick #${element_id}
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On Tab
    [Tags]
    [Documentation]    Clique sur l'onglet passé en paramètre.
    [Arguments]    ${tab}    ${tab_title}
    ${locator} =    Catenate    SEPARATOR=    css=#formulaire ul.ui-tabs-nav li a#    ${tab}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Tab Title Should Be    ${tab}    ${tab_title}
    Click Element    ${locator}
    Sleep    1
    La page ne doit pas contenir d'erreur

First Tab Title Should Be
    [Tags]
    [Arguments]    ${messagetext}
    Element Text Should Be    css=#formulaire ul.ui-tabs-nav li a    ${messagetext}

Tab Title Should Be
    [Tags]
    [Documentation]    Vérifie le titre de l'onglet.
    [Arguments]    ${tab}    ${tab_title}
    ${locator} =    Catenate    SEPARATOR=    css=#formulaire ul.ui-tabs-nav li a#    ${tab}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Element Text Should Be    ${locator}    ${tab_title}

Input Username
    [Tags]
    [Arguments]    ${username}
    Input Text    login    ${username}

Input Password
    [Tags]
    [Arguments]    ${password}
    Input Text    password    ${password}

Input HTML
    [Tags]
    [Arguments]    ${field}    ${value}
    Select Frame    ${field}_ifr
    Set Focus To Element  tinymce
    Input Text    tinymce    ${value}
    Select Window    title=${TITLE}

HTML Should Contain
    [Tags]
    [Arguments]    ${field}    ${expected}
    Wait Until Keyword Succeeds    ${TIMEOUT}    ${RETRY_INTERVAL}    Select Frame    id=${field}_ifr
    Wait Until Keyword Succeeds    ${TIMEOUT}    ${RETRY_INTERVAL}    Element Should Contain    css=#tinymce    ${expected}
    Unselect frame

HTML Should Not Contain
    [Tags]
    [Arguments]    ${field}    ${non_expected}
    Wait Until Keyword Succeeds    ${TIMEOUT}    ${RETRY_INTERVAL}    Select Frame    id=${field}_ifr
    Set Focus To Element  tinymce
    ${reel_content} =  Get Text  tinymce
    Should Not Contain  ${reel_content}  ${non_expected}
    Select Window    title=${TITLE}

Numeric Value Should Be
    [Tags]
    [Arguments]    ${champ}    ${valeurAttendue}
    ${valeurRecuperee} =    Get Text    css=#${champ}
    Should Be Equal As Integers    ${valeurAttendue}    ${valeurRecuperee}

Form Value Should Be
    [Tags]
    [Arguments]    ${champ}    ${valeurAttendue}
    ${valeurRecuperee} =    Get Value    ${champ}
    Should Be Equal    ${valeurAttendue}    ${valeurRecuperee}

Form Field Attribute Should Be
    [Tags]
    [Documentation]    Vérifie la valeur de l'attribut du champ.
    [Arguments]    ${champ}    ${attribute}    ${expected_value}
    ${get_value} =    Get Element Attribute    css=#${champ}  ${attribute}
    Should Be Equal    ${expected_value}    ${get_value}

Numeric Static Value Should Be
    [Tags]
    [Arguments]    ${champ}    ${valeurAttendue}
    ${valeurRecuperee} =    Get Text    ${champ}
    Should Be Equal As Integers    ${valeurAttendue}    ${valeurRecuperee}

Form Static Value Should Be
    [Tags]
    [Arguments]    ${champ}    ${valeurAttendue}
    ${valeurRecuperee} =    Get Text    ${champ}
    Should Be Equal    ${valeurAttendue}    ${valeurRecuperee}

Selected List Label Should Be
    [Tags]
    [Documentation]    Vérifie le libellé de l'option sélectionné.
    [Arguments]    ${field}    ${expected_value}
    ${fied_value} =    Get Selected List Label    ${field}
    Should Be Equal    ${expected_value}    ${fied_value}

Select List Should Be
    [Tags]
    [Arguments]    ${champ}    ${listeAttendue}
    ${listeRecuperee} =    Get List Items    ${champ}
    Lists Should Be Equal    ${listeAttendue}    ${listeRecuperee}

Select List Should Contain List
    [Tags]
    [Documentation]    Vérifie que la liste contient les élements passés en paramètre
    [Arguments]    ${champ}    ${listeAttendue}
    ${listeRecuperee} =    Get List Items    ${champ}
    :FOR    ${valeur}    IN    @{listeAttendue}
    \    List Should Contain Value    ${listeRecuperee}    ${valeur}

Select List Should Not Contain List
    [Tags]
    [Documentation]    Vérifie que la liste ne contient pas les élements passés en paramètre
    [Arguments]    ${champ}    ${listeInnatendue}
    ${listeRecuperee} =    Get List Items    ${champ}
    :FOR    ${valeur}    IN    @{listeInnatendue}
    \    List Should Not Contain Value    ${listeRecuperee}    ${valeur}

Link Value Should Be
    [Tags]
    [Documentation]    Vérifie le texte du lien.
    [Arguments]    ${field}    ${expected_value}
    ${get_value} =    Get Text    css=#link_${field}
    Should Be Equal    ${expected_value}    ${get_value}

Message Should Be
    [Tags]
    [Arguments]    ${messagetext}
    Element Text Should Be    css=div.message p span.text   ${messagetext}

Message Should Be In Subform
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Text Should Be  css=#sformulaire div.message p span.text  ${messagetext}

Message Should Contain
    [Tags]
    [Arguments]    ${messagetext}
    Element Should Contain    css=div.message p span.text   ${messagetext}

Message Should Contain In Subform
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  css=#sformulaire div.message p span.text  ${messagetext}

Error Message Should Be
    [Tags]
    [Arguments]    ${messagetext}
    Element Text Should Be    css=div.message.ui-state-error p span.text   ${messagetext}

Error Message Should Be In Subform
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Text Should Be  css=#sformulaire div.message.ui-state-error p span.text  ${messagetext}

Error Message Should Contain
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  css=div.message.ui-state-error p span.text  ${messagetext}

Error Message Should Contain In Subform
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  css=#sformulaire div.message.ui-state-error p span.text  ${messagetext}

Valid Message Should Be
    [Tags]
    [Arguments]    ${messagetext}
    Element Text Should Be    css=div.message.ui-state-valid p span.text   ${messagetext}

Valid Message Should Be In Subform
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Text Should Be  css=#sformulaire div.message.ui-state-valid p span.text  ${messagetext}

Valid Message Should Contain
    [Tags]
    [Arguments]    ${messagetext}
    Element Should Contain    css=div.message.ui-state-valid p span.text   ${messagetext}

Valid Message Should Contain In Subform
    [Tags]
    [Arguments]    ${messagetext}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  css=#sformulaire div.message.ui-state-valid p span.text  ${messagetext}

Get Object In Form
    [Tags]
    ${url}    Get Location
    ${url}    Fetch From Right    ${url}    obj=
    ${objInForm}    Fetch From Left    ${url}    &
    Set Suite Variable    ${objInForm}

Add File
    [Tags]
    [Arguments]  ${field}  ${file}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=#${field}_upload + a.upload > span.ui-icon
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Choose File  css=#upload-form > input.champFormulaire    ${PATH_BIN_FILES}${file}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=form#upload-form input.ui-button
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Textfield Value Should Be  css=#${field}_upload    ${file}

Add File and Expect Error Message Be
    [Tags]
    [Arguments]  ${field}  ${file}  ${message}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=#${field}_upload + a.upload > span.ui-icon
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Choose File  css=#upload-form > input.champFormulaire    ${PATH_BIN_FILES}${file}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=form#upload-form input.ui-button
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Text Should Be  css=#upload-container div.message.ui-state-error p span.text  ${message}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Link  css=form#upload-form a.linkjsclosewindow

Add File and Expect Error Message Contain
    [Tags]
    [Arguments]  ${field}  ${file}  ${message}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=#${field}_upload + a.upload > span.ui-icon
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Choose File  css=#upload-form > input.champFormulaire    ${PATH_BIN_FILES}${file}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Element  css=form#upload-form input.ui-button
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  css=#upload-container div.message.ui-state-error p span.text  ${message}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Click Link  css=form#upload-form a.linkjsclosewindow

Form Actions Should Be
    [Tags]
    [Arguments]    ${actions}
    ${length}    Get Length    ${actions}
    Log    Length = ${length}
    Xpath Should Match X Times    //div[@id="portlet-actions"]/ul/li    ${length}

    :FOR    ${index}    IN    @{actions}
    \    Element Should Contain    css=#portlet-actions ul.portlet-list   ${index}


Portlet Action Should Be In Form
    [Tags]
    [Arguments]    ${obj}    ${action}
    Page Should Contain Element    css=#form-container #portlet-actions #action-form-${obj}-${action}

Portlet Action Should Not Be In Form
    [Tags]
    [Arguments]    ${obj}    ${action}
    Page Should Not Contain Element    css=#form-container #portlet-actions #action-form-${obj}-${action}

Portlet Action Should Be In SubForm
    [Tags]
    [Arguments]    ${obj}    ${action}
    Page Should Contain Element    css=#sousform-container #portlet-actions #action-sousform-${obj}-${action}

Portlet Action Should Not Be In SubForm
    [Tags]
    [Arguments]    ${obj}    ${action}
    Page Should Not Contain Element    css=#sousform-container #portlet-actions #action-sousform-${obj}-${action}

Click On Form Portlet Action
    [Tags]
    [Arguments]    ${obj}    ${action}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=#action-form-${obj}-${action}
    Sleep    1
    La page ne doit pas contenir d'erreur

Click On SubForm Portlet Action
    [Tags]
    [Arguments]    ${obj}    ${action}
    Wait Until Keyword Succeeds     ${TIMEOUT}     ${RETRY_INTERVAL}    Click Element    css=#action-sousform-${obj}-${action}
    Sleep    1
    La page ne doit pas contenir d'erreur

Input Datepicker
    [Tags]
    [Arguments]    ${champ}    ${date}
    # On clique sur l'image du datepicker
    Click Image    css=input#${champ} + .ui-datepicker-trigger
    # On récupère le jour
    ${day} =    Get Substring    ${date}    0    2
    # On récupère le mois
    ${month} =     Get Substring    ${date}    3    5
    # On récupère l'année
    ${year} =    Get Substring    ${date}    6
    # Récupère le premier chiffre de la date
    ${day_first_character} =    Get Substring    ${day}    0    1
    # Récupère le deuxième chiffre de la date
    ${day_second_character} =    Get Substring    ${day}    1    2
    # On fait -1 sur le mois pour avoir la value du datepicker
    ${month} =    Convert to Integer    ${month}
    ${datepicker_month} =    Evaluate    ${month}-1
    ${datepicker_month} =    Convert to String    ${datepicker_month}
    # On sélectionne le mois
    Wait Until Keyword Succeeds     10 sec     ${RETRY_INTERVAL}    Select From List By Value    css=.ui-datepicker-month    ${datepicker_month}
    # On sélectionne l'année
    Select From List By Value    css=.ui-datepicker-year    ${year}
    # On sélectionne le jour, sur un caractère ou deux selon la valeur du premier
    Run keyword If    '${day_first_character}' == '0'    Click Link    ${day_second_character}    ELSE    Click Link    ${day}
    # On attend le temps que le datepicker ne soit plus affiché
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Not Be Visible  ui-datepicker-div

Input Hour Minute
    [Tags]
    [Arguments]    ${champ}    ${hour}=null    ${minute}=null
    # On sélectionne l'heure
    Run Keyword If    '${hour}' != 'null'    Select From List By Label    css=#${champ}_heure    ${hour}
    # On sélectionne la minute
    Run Keyword If    '${minute}' != 'null'    Select From List By Label    css=#${champ}_minute    ${minute}

Input Value With JS
    [Tags]
    [Arguments]    ${champ}    ${value}
    # On écrit la valeur directement dans l'attribut de l'input
    Execute JavaScript    window.jQuery("#${champ}").val('${value}');
    # On déclenche l'évènement onchange
    Execute JavaScript    window.jQuery("#${champ}").trigger("change");

Input Value With JS Failed
    [Tags]
    [Arguments]    ${champ}    ${value}    ${error}
    #
    Input Value With JS    ${champ}    ${value}
    # Vérification de l'erreur
    ${alert} =    Get Alert Message
    Should Be Equal As Strings    ${alert}    ${error}

Select Value With JS
    [Tags]
    [Arguments]  ${champ}  ${value}
    # On écrit la valeur directement dans l'attribut de l'input
    Execute JavaScript  window.jQuery("#${champ} option[value='${value}']").prop('selected', true);
    # On déclenche l'évènement onchange
    Execute JavaScript  window.jQuery("#${champ}").trigger("change");

Select Value With JS Failed
    [Tags]
    [Arguments]  ${champ}  ${value}  ${error}
    #
    Select Value With JS  ${champ}  ${value}
    # Vérification de l'erreur
    ${alert} =  Get Alert Message
    Should Be Equal As Strings  ${alert}  ${error}

Disable Event
    [Tags]
    [Arguments]  ${element}  ${event}
    Execute JavaScript  window.jQuery("#${element}").prop("${event}", null).attr("${event}", null);

Breadcrumb Should Be
    [Tags]
    [Arguments]    ${value}
    Element Text Should Be    css=#title h2    ${value}

Breadcrumb Should Contain
    [Tags]
    [Arguments]    ${value}
    Element Should Contain    css=#title h2    ${value}

Selected Tab Title Should Be
    [Tags]
    [Arguments]    ${id}    ${libelle}
    Element Text Should Be    css=li.ui-tabs-selected #${id}    ${libelle}

Select Checkbox From List
    [Tags]
    [Documentation]    Sélectionne une liste de case à cocher.
    [Arguments]    @{list_checkbox}
    :FOR    ${checkbox}    IN    @{list_checkbox}
    \    Select Checkbox    ${checkbox}

Form Value Should Contain From List
    [Tags]
    [Documentation]    Vérifie la présence d'élément dans un champ de formulaire
    ...    depuis une liste.
    [Arguments]    ${field}    @{list_expected}
    :FOR    ${element}    IN    @{list_expected}
    \    Element Should Contain    ${field}    ${element}

Form HTML Should Contain From List
    [Tags]
    [Documentation]    Vérifie la présence d'élément dans un champ HTML de
    ...    formulaire depuis une liste.
    [Arguments]    ${field}    @{list_expected}
    Select Frame    ${field}_ifr
    Set Focus To Element  tinymce
    :FOR    ${element}    IN    @{list_expected}
    \    Element Should Contain    tinymce    ${element}
    Select Window    title=${TITLE}

Open Fieldset
    [Tags]
    [Documentation]    Déplie un fieldset et attend qu'il soit ouvert
    [Arguments]    ${obj}    ${fieldset}
    # Modification de la méthode de clic sur un élément. Il semble qu'en fonction
    # de l'environnement le clic sur l'élément legend du fieldset ne fonctionne
    # pas toujours. Le clic sur l'élément est donc simulé par l'appel à une
    # fonction javascript permettant d'afficher le bloc du fieldset.
    #Click Element    css=#fieldset-form-${obj}-${fieldset} > legend.collapsible
    Execute JavaScript  window.jQuery("#fieldset-form-${obj}-${fieldset} > div.fieldsetContent").attr("style", "display:table;");
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Be Visible  css=#fieldset-form-${obj}-${fieldset} > div.fieldsetContent

Open Fieldset In Subform
    [Tags]
    [Documentation]    Déplie un fieldset et attend qu'il soit ouvert
    [Arguments]    ${obj}    ${fieldset}
    # Modification de la méthode de clic sur un élément. Il semble qu'en fonction
    # de l'environnement le clic sur l'élément legend du fieldset ne fonctionne
    # pas toujours. Le clic sur l'élément est donc simulé par l'appel à une
    # fonction javascript permettant d'afficher le bloc du fieldset.
    #Click Element    css=#fieldset-sousform-${obj}-${fieldset} > legend.collapsible
    Execute JavaScript  window.jQuery("#fieldset-sousform-${obj}-${fieldset} > div.fieldsetContent").attr("style", "display:table;");
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Be Visible  css=#fieldset-sousform-${obj}-${fieldset} > div.fieldsetContent

Select Multiple By Label
    [Tags]
    [Documentation]    Sélectionne une liste de libellés si non vide
    [Arguments]  ${champ}  ${list}
    ${length} =  Get Length  ${list}
    Run Keyword If  ${length} > 0  Select From List By Label  ${champ}  @{list}

Element Should Contain In Subform
    [Tags]
    [Arguments]  ${element}  ${string}
    Wait Until Element Is Visible  ${element}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Element Should Contain  ${element}  ${string}

Element Text Should Not Be
    [Tags]
    [Arguments]  ${element}  ${non_expected}
    Wait Until Element Is Visible  ${element}
    ${reel_content} =  Get Text  ${element}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Should Not Be Equal As Strings  ${reel_content}  ${non_expected}

Element Should Not Contain
    [Tags]
    [Arguments]  ${element}  ${non_expected}
    Wait Until Element Is Visible  ${element}
    ${reel_content} =  Get Text  ${element}
    Wait Until Keyword Succeeds  ${TIMEOUT}  ${RETRY_INTERVAL}  Should Not Contain  ${reel_content}  ${non_expected}

Set Checkbox
    [Tags]
    [Arguments]  ${element}  ${value}='true'
    Run Keyword If  '${value}' == 'true'  Select Checkbox  ${element}
    Run Keyword If  '${value}' == 'false'  Unselect Checkbox  ${element}

Element Must Be Disabled
    [Tags]
    [Arguments]  ${element_id}
    ${value} =  Get Element Attribute  ${element_id}  disabled
    Should Be Equal  ${value}  true

Element Must Be Enabled
    [Tags]
    [Arguments]  ${element_id}
    ${value} =  Get Element Attribute  ${element_id}  disabled
    Should Be Equal  ${value}  ${None}

Element should contain X times
    [Tags]
    [Arguments]  ${locator}  ${string}  ${count}
    Wait Until Element Is Visible  ${locator}
    ${reel_content} =  Get Text  ${locator}
    Should Contain X Times  ${reel_content}  ${string}  ${count}

Get Mandatory Value
    [Tags]
    [Arguments]  ${locator}
    :FOR  ${i}  IN RANGE  20
    \  ${value_not_empty} =  Get Value  ${locator}
    \  # Renvoie la valeur si elle n'est pas vide
    \  Return From Keyword If  "${value_not_empty}" != "${null}"  ${value_not_empty}
    \  Sleep  1
    \  ${i} =  Set Variable  ${i} + 1
    Fail

Element Should Contain From List
    [Tags]
    [Documentation]    Vérifie la présence d'une liste de string dans un élément.
    [Arguments]    ${element}    ${list_expected}
    :FOR    ${text}    IN    @{list_expected}
    \    Element Should Contain    ${element}    ${text}


Le portlet d'action ne doit pas être présent dans le sous-formulaire
    [Documentation]  Vérifie que le portlet d'action n'est pas affiché.

    Page Should Not Contain Element  css=#sousform-container div#portlet-actions
