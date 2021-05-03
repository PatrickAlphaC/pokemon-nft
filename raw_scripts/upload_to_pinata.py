import requests
import os
from pathlib import Path
import json
import time

PINATA_BASE_URL = 'https://api.pinata.cloud/'
endpoint = 'pinning/pinFileToIPFS'
# Change this to upload a different file
filepath = './img/pokemon_images'
headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
           'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}


def main():
    pokemon_images_path = Path(filepath).glob('**/*.png')
    for pokemon_path in pokemon_images_path:
        filename = str(pokemon_path).split('/')[-1:][0]
        upload_to_pinata(pokemon_path, filename=filename)


def upload_to_pinata(pokemon_path, filename=None):
    with pokemon_path.open("rb") as fp:
        image_binary = fp.read()
        filename = filename if filename else pokemon_path
        print(f"Uploading {filename}")
        try:
            response = requests.post(PINATA_BASE_URL + endpoint,
                                     files={"file": (filename, image_binary)},
                                     headers=headers)
            print(response.json())
        except json.decoder.JSONDecodeError:
            print("Whoops, ran into an issue")
            time.sleep(5)
            upload_to_pinata(pokemon_path, filename=filename)


if __name__ == '__main__':
    main()
