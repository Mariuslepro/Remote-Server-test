import paramiko


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
