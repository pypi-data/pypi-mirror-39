import os
import io
import sys
import zipfile
import pathlib
import requests
import pandas as pd


def save_zip(content, dir):
    with zipfile.ZipFile(file=io.BytesIO(content)) as zip:
        zip.extractall(dir)


def check_dir(dir):
    if not os.path.exists(dir):
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


def get_header(url, dir, file):
    req = requests.get(url)
    html = pd.read_html(req.content)
    df = html[0].transpose().iloc[:1, 1:]
    df.to_csv(path_or_buf=os.path.join(dir, file), index=False, header=False)


def print_to_shell(message):
    sys.stdout.write(message + "\n")
