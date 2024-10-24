    *** Settings ***
Library    remote_command_library.py

*** Variables ***
 #Define the server's connection parameters
 
 #Exemple:
${hostname}    192.168.137.2
${port}    ${22}
${username}    serverusername
${password}    motdepass


*** Test Cases ***

Get Rebootserver

    Reboot server remotely    ${hostname}    ${port}    ${username}    ${password}
    sleep    60s
    
    ${result} =    type16 smbios2    ${hostname}    ${port}    ${username}    ${password}
    Log    ${result}

    ${result} =    type17 smbios2    ${hostname}    ${port}    ${username}    ${password}
    Log    ${result}

    ${result} =    Get pcie info2    ${hostname}    ${port}    ${username}    ${password}
    Log    ${result}
