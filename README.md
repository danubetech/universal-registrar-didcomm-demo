# Purpose

This is a demo for aries-cloudagent-python.
It connects two agents via didcomm, and then sends a did registration request
from one agent to the other agent. For the DID registration
https://uniregistrar.io is used.

# Run the demo

For a basic (insecure) demo on localhost:
```
# install (debian) packages, pip and virtualenv:
sudo apt install python3-virtualenv python3-pip
# or alternatively: pip install virtualenv
# install aries-cloudagent including the did registration protocol
mkdir venv
virtualenv -p python3 venv/
source venv/bin/activate
pip install -r requirements.txt
git clone git@github.com:danubetech/universal-registrar-didcomm.git
cd universal-registration-didcomm
git checkout main
pip install --no-cache-dir -e .
pip install python3-indy
```

When running the docker demo, first build the docker image inside the aries-cloudagent-python folder:
`docker build . -f docker/Dockerfile.did_registration_demo -t universalregistrar/universal-registrar-didcomm-demo:latest`

Then start two agents, acting as a server and a client (in a separate shell after activating the virtualenv again):
```
# server
aca-py start -it http 127.0.0.1 3555 -ot http --auto-accept-invites --auto-accept-requests --endpoint http://127.0.0.1:3555 --auto-respond-messages --label Server --log-level debug --public-invite --invite --invite-base-url http://localhost:3555 --invite-multi-use --no-ledger --admin-insecure-mode --admin 127.0.0.1 3000 --write-invitation-to=~/didcomm-invitation.txt --emit-new-didcomm-prefix
# docker server (image built with aries-cloudagent-container), listening on and mapping port 3555:
docker run --net=host -p 3000:3000 -p 3555:3555 -i -t universalregistrar/universal-registrar-didcomm-demo:latest start --admin-insecure-mode --admin 0.0.0.0 3000 -it http 0.0.0.0 3555 -ot http --auto-accept-invites --auto-accept-requests --endpoint http://0.0.0.0:3555 --auto-respond-messages --label Server --log-level debug  --public-invite --invite --invite-base-url http://localhost:8080 --no-ledger --emit-new-didcomm-prefix

When using docker you currently have to copy/paste the invitation manually, or use docker volumes.

# client (will execute the didcomm queries)
aca-py start --admin-insecure-mode --admin 127.0.0.1 4000 -it http 127.0.0.1 4555 -ot http --auto-accept-invites --auto-accept-requests --endpoint http://127.0.0.1:4555 --auto-store-credential --auto-respond-messages --label Client --auto-ping-connection --log-level debug --no-ledger --emit-new-didcomm-prefix
# docker client
docker run --net=host -p 4000:4000 -p 4555:4555 -i -t universalregistrar/universal-registrar-didcomm-demo:latest start --admin-insecure-mode --admin 0.0.0.0 4000 -it http 0.0.0.0 4555 -ot http --auto-accept-invites --auto-accept-requests --endpoint http://0.0.0.0:4555 --auto-store-credential --auto-respond-messages --label Client --auto-ping-connection --log-level debug --no-ledger --emit-new-didcomm-prefix
```

Finally run `register_did.py` to connect the agents, and tell the client to
send a did registration request to the server:

```
python3 register_did.py --invitation-path=~/didcomm-invitation.txt
# alternatively, use the base64 encoded invitation directly (e.g. when running with docker):
python3 register_did.py --invitation="eyJAdHlw..."
```

In the log of the server you should see the did registration request arriving,
and on the client you should then see the registration result of the didcomm
message.

# Websocket demo

Similar to above, the main difference is to start the server like this:
aca-py start -it ws 127.0.0.1 3555 -ot ws --auto-accept-invites --auto-accept-requests --endpoint ws://127.0.0.1:3555 --auto-respond-messages --label Server --log-level debug --public-invite --invite --invite-base-url ws://localhost:3555 --invite-multi-use --no-ledger --admin-insecure-mode --admin 127.0.0.1 3000 --write-invitation-to=~/didcomm-invitation.txt --no-ledger --emit-new-didcomm-prefix

And the client:
aca-py start --admin-insecure-mode --admin 127.0.0.1 4000 -it ws 127.0.0.1 4555 -ot ws --auto-accept-invites --auto-accept-requests --endpoint ws://127.0.0.1:4555 --auto-store-credential --auto-respond-messages --label Client --auto-ping-connection --log-level debug --no-ledger

# websocket demo with hard-coded seed / invitation
Not yet working; start server without --invite-multi-use but with --invite-public:
Server:
aca-py start -it ws 127.0.0.1 3555 -ot ws --auto-accept-invites --auto-accept-requests --endpoint ws://127.0.0.1:3555 --auto-respond-messages --label Server --log-level debug --public-invite --invite --public-invites --invite-public --invite-base-url ws://localhost:3555 --seed 12345678912345678912345678912345
Client:
aca-py start --admin-insecure-mode --admin 127.0.0.1 4000 -it ws 127.0.0.1 4555 -ot ws --auto-accept-invites --auto-accept-requests --endpoint ws://127.0.0.1:4555 --auto-store-credential --auto-respond-messages --label Client --auto-ping-connection --log-level debug

instead, write to 'invitation.txt' for now.
