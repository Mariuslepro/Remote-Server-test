readme

============================================================================
REMOTELY EXECUTE COMMAND ON A DISTANT PC AND GET THE ROBOTFRAMEWORK report
============================================================================
============================================================================
REMOTELY CONNECT TO SERVER, RUN REBOOT STRESS THEN RETRIEVE INFORMATIONS 
SUCH AS: PCIE DEVICES, SMBIOS TYPE 16, SMBIOS TYPE 17 AND GET THE 
ROBOTFRAMEWORK report
============================================================================

Tools: robotframework; Pycharm; PowerShell; Python; Windows; MacOS 


    The test will have 3 steps: the creation and configuration of the network,
the code's writing, the execution of the test.

I- Creation and configuration of the network

The test has been done in a LAN of two pc (PC1 and PC2).
NB: One of the PC most be a server and the other the client

I-1 LAN's creation
------------------

I-1-1 Methode 1: Setting up an Ethenet LAN
------------------------------------
    Connect PC1 and PC2 by RJ45 cable then setup the network properties to 
allow the communiation.

I-1-2 Methode 2: Setting up an W-LAN
------------------------------

PC1 will be the hotspot and will host the connexion.
* Make sure PC1 can be a hotspot. 
    - Open PowerShell or the cmd.
    - type the command: 'netsh wlan show driver'.
    - Make sure the line "Hosted network supported  : yes" has yes as 
    result
* Create the w-lan on PC1
    - Open PowerShell or the cmd.
    - Type this command to create the wlan: netsh wlan set hostednetwork
     mode=allow ssid=networktest key=motdepass
        NB: networktest = 'name of your network', and motdepass = 'your 
        mot de password'
    - Type this command to start the wlan: NETSH WLAN START HOSTEDNETWORK
* Connect the two PC by searching the wlan from PC2 and entering the 
password 

  Now, the PCs are connected on the same network, they can communicate 
  together. you can type 'ipconfig' in the powershell the see the actual
   configuration. You can also manually setup ip adddress and others

I-2 PCs's configuration
----------------------
  In order to communicate efficiently, one of the PC most be the server 
  and the other the client.
  we will acivate the openSSHserver on one of the PC. Let say PC1.
  * Setting up PC1 as server
    - Open PowerShell
    - type the following commands




  ....


At this level, the client can be conected to the server and must be able to 
execute commands.
The goal here is to SSH into the server, reboot it, then retrieve informations
 such as:
 - PCIE's numbers
 - PCIE'devices list
 - SmBios Type 16
 - SmBios Type 17
then return these informations and possible bugs in a robotFramework's report file

=================
PROJECT'S files
=================
This project contains 3 files: remote_command.robot,
 remote_command_library.py and this readme.rst

1. remote_command.robot
-----------------------
The keyword-driven testing approach is use here. This robot code contains 
a workflow constructed from keywords from a python file 
remote_command_library.py.
This code manually gets the information(IP address, port...) to reach the
server, then calls methods from the library remote_command_library.py to
obtain all needed information.
Then generates the report and the log files 


2. remote_command_library.py
------------------------
This is the python library. It contains the methods 
to establish the connection with the server, and retrieve the information's
needed.

=======
CODES
=======

Creating test libraries
=======================

.. code:: python
    import datetime
    import os
    import subprocess
    import re
    import paramiko_test

class lspci_test_Library: 

    def find_sentences_with_word2(file_path, word):
        sentences_with_word = []

        # Ouvrir le fichier en mode lecture
        f = open(file_path, "r")
        lines = f.read()
        lines = lines.splitlines()
        lines = filter(None, lines)
        #print(lines)

        for li in lines:
            if str(li).startswith(word):
                sentences_with_word.append(str(li).split(':'))
        print("find sentences")
        print(sentences_with_word)
        print('find')
        return sentences_with_word

    def launch_lspci_paramiko(self):


        lspci_output_file = r"C:\Users\Mariuslepro\PycharmProjects\ProjectVenv\Harold-test\lspci_output_file.txt"
        command = r"Pnputil.exe /enum-drivers"
        result = paramiko_test.connexion(command)
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

        # Écrire la sortie dans le fichier
        with open(lspci_output_file, 'w') as output_file:
            output_file.write(result)

        output_file.close()
        publisher_name = lspci_test_Library.find_sentences_with_word2(lspci_output_file, "Published")
        return publisher_name


.. code:: robotframework
    *** Settings ***
    Library    lspci_test_Library.py
    Library           Collections
    Library    BuiltIn

    *** Variables ***
    ${duration}    15
    ${delay}    5
    ${count}    ${duration}/${delay}
    ${separator}    \n

    *** Test Cases ***
        
    Get Lspci
        FOR    ${i}    IN RANGE    ${count}
            ${list} =    Launch Lspci paramiko
            #Log    ${list}
            FOR  ${lix}  IN  @{list}
                Log    ${lix}
            END

            Sleep  5s
        END
