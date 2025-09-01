```bash
ssh -i ayush.pem ubuntu@<ip>
```
```bash
sudo apt update && sudo apt upgrade
```

```bash 
git clone https://github.com/ayushacharya27/aws-proj-backend
```

```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
```

```bash
ngrok config add-authtoken 323jsMUkcCmqik3YsVxTqv5agMs_2fLynh858caZugJGRgZq1
```

```bash
nano .config/ngrok/ngrok.yml
```

### Paste this
```bash
version: "3"
agent:
  authtoken: 323jsMUkcCmqik3YsVxTqv5agMs_2fLynh858caZugJGRgZq1

tunnels:
  ayush-app:
    addr: 8000
    proto: http
    hostname: champion-normal-raven.ngrok-free.app
```

```bash
cd aws-proj-backend && git checkout master
```

```bash
source aws-project-env/bin/activate
```

```bash
nohup python3 test.py &
```

```bash 
ngrok start ayush &
```

