*** Settings ***
Library  library/Base.py



*** Test Cases ***
Test that a user can be added to the database
    [Documentation]  Ensures that the database has been configured correctly.
    Create user called  Fred

Test that a user can make a request
    [Documentation]  Ensures that the database has been configured correctly.
    @{TAGS} =  Create list  tag1  tag2  tag3
    Create user called  Fred
    They make a request with tags  @{TAGS}
    ${THEIR_REQUESTS}  Call method  ${LAST_USER}  requests
    Should contain x times  ${THEIR_REQUESTS}  ${LAST_REQUEST}  1

Test that a user can have their tags set
    [Documentation]  Ensures that tags can be set to, and read from, the database correctly.
    Create User  Fred
    @{ORIG_TAGS} =  Create List  tag1  tag2  tag3
    Set their tags  @{ORIG_TAGS}
    @{DB_TAGS} =  Get their tags
    Should be equal  @ORIG_TAGS}  @{DB_TAGS}

Test that a user

*** Keywords ***
Create User called
    [Arguments]  ${USER}
    ${LAST_USER} =  Create user directly  ${LAST}
    Set test variable  ${LAST_USER}  ${LAST_USER}

Set their tags
    [Arguments]  @{TAGS}
    Set user tags  ${User}  @{TAGS}

Get their tags
    [return]  Get user tags  ${LAST_USER}

They make a request with tags
    [Arguments]  @{TAGS}
    ${LAST_REQUEST}  Create request directly  @{TAGS}  ${LAST_USER}
    Set test variable  ${LAST_REQUEST}  ${LAST_REQUEST}


