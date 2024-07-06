sudo apt-get install -y git nodejs



python -m venv .venv
. .venv/bin/activate

pip install wheel
. python/add_path_to_venv.sh

pip install -r testjig/python/requirements.txt



