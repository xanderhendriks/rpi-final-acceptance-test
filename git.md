Setup laptop
It is recommended to use ssh login and to forward the ssh certificate using an ssh-agent. For windows:

Run PowerShell in Administrator mode.

Enable the ssh-agent if not already done so:



Get-Service ssh-agent | Set-Service -StartupType Automatic -PassThru | Start-Service
start-ssh-agent.cmd
It may run a different terminal. exit to return to the PowerShell terminal.

Add your key to the agent:



ssh-add c:\Users\<user>\.ssh\id_rsa
You can check it’s been added using:



ssh-add -l
Login to the testjig with Enable forwarding of the authentication agent connection (-A):



ssh pi@fw-jig-1 -A
Test the connection by running the following command on the testjig:



ssh -T git@github.com


git config --global user.email fw-jig-1@sitehive.co
git config --global user.name fw-jig-1
git config --global pull.ff only