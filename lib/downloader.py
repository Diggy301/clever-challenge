import requests
import pathlib
import os
import zipfile


class Downloader:
    """
    A class to handle downloading Zipfiles from a specified URL
    """
    def __init__(self, dir: pathlib.Path) -> None:
        """
        Initializes the Downloader with the base URL and temporary directory.

        :param dir: The directory where downloaded files will be stored.
        """
        self.dir = dir

    def download_file(self, download_url: str) -> None:
        """
        Downloads a file from the specified URL and saves it to the designated directory.

        :param download_url: The URL of the file to be downloaded.
        """
        filename = download_url.split("/")[-1]
        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status() # Raise an error for bad responses (4xx or 5xx)

            filepath = os.path.join(self.dir, filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded successfully: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file: {e}")

    
    def extract_zip_file(self, zip_path: pathlib.Path, extract_to: pathlib.Path) -> None:
        """
        Extracts the contents of a Zip file to the specified directory.

        :param zip_path: The path to the Zip file to be extracted.
        :param extract_to: The directory where the contents will be extracted.
        """
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
                print(f"Extracted: {zip_ref}")
        except zipfile.BadZipFile:
            print(f"Error: {zip_ref} is not a valid Zip file.")
