import click
from connect import connect_agents
import requests
from config import client_url
import urllib


def register_did(base_url, connection_id):
    url = urllib.parse.urljoin(base_url,
                               f"connections/{connection_id}/register-did")
    content = {
        "@type": "https://didcomm.org/did_registration/0.1",
        "@id": "xhqMoTXfqhvAgtYxUSfaxbSiqWke9t",
        "driver_id": "driver-universalregistrar/driver-did-key",
        "secret": {},
        "job_id": None,
        "options": {
            "keyType": "Ed25519VerificationKey2018"
        },
        "did_document": {
            "service": [],
            "verificationMethod": [],
            "authentication": []
        }
    }
    requests.post(url, json=content)


@click.command()
@click.option('--invitation-path', default=None,
              help='path of the invitation file.')
@click.option('--invitation', default=None, help='base64-encoded invitation.')
def main(invitation_path, invitation):
    connection_id = connect_agents(invitation_path=invitation_path,
                                   invitation=invitation)
    register_did(client_url, connection_id)


if __name__ == '__main__':
    main()
