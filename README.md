# Introduction
This is the second part of a two part workshop. The first part and introduction can be found in the following repository: [xanderhendriks/rpi-embedded-target-action-runner](https://github.com/xanderhendriks/rpi-embedded-target-action-runner).

It uses the same [hardware](https://github.com/xanderhendriks/rpi-embedded-target-action-runner?tab=readme-ov-file#hardware-used) and assumes the SD Card for the RFaspberry Pi is prepared as described in [preparing-the-sd-card](https://github.com/xanderhendriks/rpi-embedded-target-action-runner?tab=readme-ov-file#preparing-the-sd-card)

# Software used
Install the following software locally:
- [WinSCP](https://winscp.net/eng/download.php)

# Accounts used
- [Github](https://github.com/)

# Fork the workshop repository
Fork the [xanderhendriks/rpi-embedded-target-action-runner](https://github.com/xanderhendriks/rpi-final-acceptance-test) repository:

![Github fork](images/Github_fork.png)

# Install the RPi software
## SSH login
login to the RPi using ssh. Add the -L to forward port 22 to allow sftp file transfer on localhost. And add the -A option for ssh agent forwarding to the RPi. This will allow you to use your github ssh certificate without having to transfer it to the RPi. Check [ssh-agent-forwarding](ssh-agent-forwarding.md) to see how to set this up:

    ssh pi@nxs-<RPi identifier> -A -L 22:nxs-<RPi identifier>:22

## Fork the workshop repo
Once logged in clone your fork in the /home/pi directory:

    git clone git@github.com:<your_github_username>/rpi-final-acceptance-test.git

## Configure git
    git config --global user.email <your-email>
    git config --global user.name <your-user-name>
    git config --global pull.ff only

## Installing NodeJS
[Node.js](https://nodejs.org/en) is a free, open-source, cross-platform JavaScript runtime environment that lets developers create servers, web apps, command line tools and scripts. It is used by [React](https://react.dev/), the library for web and native user interfaces. As the RPi comes with a rather old version it is updated to version 18 to work with the code in this project:

    curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs

## Installing yarn
[Yarn](https://classic.yarnpkg.com/en/) is a package manager that doubles down as project manager:

    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    sudo apt update
    sudo apt install -y yarn

## Installing the redis server
Redis (REmote DIctionary Server) is an open source, in-memory, NoSQL key/value store that is used primarily as an application cache or quick-response database. It is used here for displaying the logging messages in the GUI:

    sudo apt install -y redis-server
    sudo systemctl enable redis-server
    sudo systemctl start redis

# Setup Python
    cd ~/rpi-final-acceptance-test
    python -m venv .venv
    . .venv/bin/activate

## Install dependencies
    pip install wheel
    . python/add_path_to_venv.sh
    pip install -r testjig/python/requirements.txt

# Create a symbolic link for the api
    ln -s $PWD/testjig/react-flask-app/python testjig/react-flask-app/api

# Setup the React project
    cd testjig/react-flask-app
    yarn install

# Start in debug mode
## Python API
    yarn start-api

## React test server
Start a second terminal:

    ssh pi@localhost
    cd ~/rpi-final-acceptance-test/testjig/react-flask-app
    yarn start

The React server will show the url to use for accessing it on port 3000

# Build the code and run

    yarn build
    sudo ln -s ~/rpi-final-acceptance-test/testjig/react-flask-app.service /etc/systemd/system/react-flask-app.service
    sudo systemctl enable react-flask-app
    sudo systemctl start react-flask-app









