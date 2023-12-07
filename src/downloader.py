import os
import requests
from tqdm import tqdm
from urllib.parse import urlsplit
from http.client import IncompleteRead


def check_url_availability(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def make_request(url, stream=True, allow_redirects=True, headers=None):
    try:
        response = requests.get(
            url, stream=stream, allow_redirects=allow_redirects, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            return response

        return None
    except (requests.exceptions.RequestException, IncompleteRead) as e:
        print(f"Request error: {e}")
        return None


def download_with_progress(response, destination, chunk_size=1024 * 1024, unit='KB', unit_scale=True, unit_divisor=1024):
    total_size = int(response.headers.get('content-length', 0))

    with tqdm(total=total_size, unit=unit, unit_scale=unit_scale, unit_divisor=unit_divisor) as progress_bar:
        with open(destination, 'ab' if os.path.exists(destination) else 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))


def download_file_from_url(url, base_folder="."):
    try:
        response = make_request(url)
        if response is None:
            print(f"The file is not available at the URL: {url}")
            return

        parts_of_url = urlsplit(url).path.split('/')
        version = parts_of_url[-3]
        platform = parts_of_url[-2]
        filename = parts_of_url[-1]

        destination_folder = os.path.join(
            base_folder, "downloads", version, platform)
        os.makedirs(destination_folder, exist_ok=True)
        destination_path = os.path.join(destination_folder, filename)

        if os.path.exists(destination_path):
            print(
                f"The file already exists at {destination_path}. Use the 'overwrite=True' option to overwrite.")
            return

        download_with_progress(response, destination_path)

        print(f"\nSuccessfully downloaded file at: {destination_path}")
        print(
            f"File size: {os.path.getsize(destination_path) / (1024 * 1024):.2f} MB")
    except Exception as e:
        print(f"Error downloading the file: {e}")


def download_selected_files(urls):
    for url in urls:
        download_file_from_url(url)
