import logging
import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("data-photo_max")
        if not img_url:
            continue

        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)
    return urls


def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, url.split("/")[-1])
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True,
                    unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))


def download_treatment_photos(url, path):
    imgs = get_all_images(url)
    unique = []
    for img in imgs:
        if img not in unique:
            unique.append(img)
            download(img, path)


logging.basicConfig(level=logging.INFO, filename='data/downloadingInvisalign.log', filemode='a',
                    format='%(levelname)s: %(message)s')

for i in range(1,1722):
    i = str(i)
    url = 'https://global.invisaligngallery.com/treatment/t-' + i
    try:
        download_treatment_photos(url, 'raw_data/Invisalign/' + i)
        logging.info('Images of patient ' + i + ' have been downloaded')
    except:
        logging.error('Something went wrong when downloading images of patient ' + i)
