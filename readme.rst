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
    import paramiko_test



class remote_command_library:

    # takes server's parameters, to connect To the Server, Execute the Command and return
    # result if needed in a string
    def connecToServerExecuteCommand(self, hostname, port, username, password, command) -> str:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()

        # Automatically add the remote server's SSH key (dangerous in production)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the remote server
            ssh.connect(hostname, port, username, password)
            # Execute a command
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read().decode()
            # Print the command output
            # print(stdout.read().decode())
            # Print any error messages
            #print(stderr.read().decode())

        finally:
            # Close the connection
            ssh.close()

        return result

    # Working on windows pc

    # Reboot a Windows server
    def reboot_server_remotely(self, hostname, port, username, password):
        command = r"shutdown /r /t 0"
        remote_command_library.connecToServerExecuteCommand(self, hostname, port, username, password, command)

    # Return the Network Interface Information on MWindows
    def get_network_info2(self, hostname, port, username, password) -> str:
        command = r"ipconfig"
        result = remote_command_library.connecToServerExecuteCommand(self, hostname, port, username, password, command)
        return result

    def get_pcie_info2(self, hostname, port, username, password) -> str:

        #Numbers of pcie's devvices
        command2 = 'wmic path win32_pnpentity where "DeviceID like \'%PCI%\'" get Name,DeviceID | find /c /v ""'
        result2 = "\n the number of PCIE is: " + remote_command_library.connecToServerExecuteCommand(self, hostname,
                                                                                                     port, username,
                                                                                                     password, command2)

        # Get pcie,s devices info
        #command = "wmic path win32_pnpentity get name, deviceid | findstr PCI "
        command = 'wmic path win32_pnpentity where "DeviceID like \'%PCI%\'" get Name,DeviceID'
        result = "\n List of PCI Equipments: \n" + remote_command_library.connecToServerExecuteCommand(self, hostname,
                                                                                                       port, username,
                                                                                                       password,
                                                                                                       command)
        return result2 + result

    #Get the Smbios type16
    def type16_smbios2(self, hostname, port, username, password) -> str:
        # type 16
        command = r"wmic memorychip get BankLabel, Capacity, DeviceLocator, MemoryType, TypeDetail, FormFactor, DataWidth, Status"
        #command =r"wmic memorychip list full"
        result = remote_command_library.connecToServerExecuteCommand(self, hostname, port, username, password, command)
        return result

    #Get the Smbios type17
    def type17_smbios2(self, hostname, port, username, password) -> str:
        # type 17
        command = r"wmic memorychip get BankLabel, Capacity, DeviceLocator, Manufacturer, PartNumber, Speed, SerialNumber"
        result = remote_command_library.connecToServerExecuteCommand(self, hostname, port, username, password, command)
        return result


.. code:: robotframework
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

