echo 'Installing venv...'
pip install  virtualenv .
echo  'Creating virtual env...'
virtualenv -p python3 qkdenv
source qkdenv/bin/activate
echo 'Installing required packages...'
pip install -r requirements.txt
ipython kernel install --name "qkdenv" --user