export LC_ALL=C
sudo locale-gen en_US en_US.UTF-8
sudo dpkg-reconfigure locales 
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip python3-tk -y
pip3 install spacy textacy 
pip3 install numpy matplotlib 
pip3 install jupyter ipykernel  
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_lg
git clone https://github.com/tonghuikang/given-text-detect-claim-api/

cd given-text-detect-claim-api
jupyter nbconvert --to python process_claims.ipynb
python3 process_claims.py
python3 server.py
