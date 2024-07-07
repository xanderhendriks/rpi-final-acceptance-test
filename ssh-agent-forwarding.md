# ssh agent forwarding
ssh agent forwarding allows you to forward the github ssh certificate through an ssh connection without having to copy it to the device.

# Laptop setup
Run PowerShell in Administrator mode.

Enable the ssh-agent if not already done so:

    Get-Service ssh-agent | Set-Service -StartupType Automatic -PassThru | Start-Service
    start-ssh-agent.cmd

It may run a different terminal. exit to return to the PowerShell terminal.

# Adding github key
Add your key to the agent:

    ssh-add c:\Users\<user>\.ssh\id_rsa

You can check it’s been added using:

    ssh-add -l

# Login with forwarding
Login to the Rpi with Enable forwarding of the authentication agent connection (-A):

    ssh pi@nxs-<device_identifier> -A

Test the connection by running the following command on the RPi:

    ssh -T git@github.com
