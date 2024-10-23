*** Settings ***
Library    remote_command_library.py

*** Variables ***
 #Define connection parameters
 #My MacOS parameters
#${hostname}    192.168.137.3
#${port}    ${22}
#${username}    apple
#${password}    12345

 #My windows parameters
#${hostname}    192.168.137.2
#${port}    ${22}
#${username}    mariuslepro
#${password}    mariuslepro

${hostname}    127.0.0.1
${port}    ${22}
${username}    mariuslepro
${password}    mariuslepro

*** Test Cases ***

Get Rebootserver

    #Reboot server remotely    ${hostname}    ${port}    ${username}    ${password}
    #sleep    60s
    
    ${result} =    type16 smbios2    ${hostname}    ${port}    ${username}    ${password}
    Log    ${result}

    ${result} =    type17 smbios2    ${hostname}    ${port}    ${username}    ${password}
    Log    ${result}

    ${result} =    Get pcie info2    ${hostname}    ${port}    ${username}    ${password}
    Log    ${result}
