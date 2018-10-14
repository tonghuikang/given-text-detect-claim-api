# given-text-detect-claim-api
Finally making this into an API

### Cloud installation script
Setup Ubuntu 16.04, 20GB disk space, enable http and https.

```
curl https://raw.githubusercontent.com/tonghuikang/given-text-detect-claim-api/master/install.sh | sudo bash
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
