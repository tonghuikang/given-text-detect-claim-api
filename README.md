# given-text-detect-claim-api
Finally making this into an API

### Cloud installation script

```
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip python3-tk
pip3 install spacy textacy 
pip3 install numpy matplotlib 
pip3 install jupyter ipykernel  
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_lg
git clone https://github.com/tonghuikang/given-text-detect-claim-api/
```

### Preprocess the list of claims
```
jupyter nbconvert --to python process_claims.ipynb
python3 process_claims.py
```

### Script to start a server
```
cd given-text-detect-claim-api
python3 server.py
```

### To use the api

Send a json POST request to `cloud.ext.ip.addr:4000`
```
{"article_text" : "Donald Trump made fun of a disabled reporter."}
```
