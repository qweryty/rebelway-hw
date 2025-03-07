import os
import re
from typing import Any
import requests
import hou

CHUNK_SIZE = 32768
GDRIVE_URL = "https://drive.google.com/uc"

# works with direct links and share links
ID_PATTERN = re.compile(
    r"(?:drive\.google\.com\/(?:file\/d\/|uc\?id=))([a-zA-Z0-9_-]+)"
)


def download_gdrive_asset(
    url: str = "https://drive.google.com/file/d/125k5-81AY7B5RkGqKjAo7fVM-Gw3tOQh/view?usp=sharing",
    destination: str = "$HIP/downloads/monkey.abc",
):
    destination = hou.expandString(destination)
    # extracting file url
    match = ID_PATTERN.search(url)
    if not match:
        raise ValueError("Incorrect url")

    file_id = match.group(1)

    # preparing directory
    target_dir = os.path.dirname(destination)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    session = requests.Session()
    response = session.get(
        GDRIVE_URL,
        params={"export": "download", "confirm": "1", "id": file_id},
        stream=True,
    )
    token = None
    # confirming download
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(url, params=params, stream=True)

    # downloading data
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download(kwargs: dict[str, Any]):
    node: hou.OpNode = kwargs["node"]
    url = node.parm("url").eval()
    file = node.parm("file").eval()

    download_gdrive_asset(url=url, destination=file)
