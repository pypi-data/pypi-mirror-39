import requests
import os
from . import unzip
from .dataset_retriver import RiksDatasetInterface


class RiksDatasetDownloader:

    def __init__(self, interface=RiksDatasetInterface):
        self.unzipper = unzip
        self.interface = interface

    def download_dataset(self, url, directory, unzipper=unzip, verbose=False):
        """ Download a dataset and save it to path. """
        # Download the data
        data = requests.get(url)

        # Escape if URL is wrong
        if not data.ok:
            print("Could not download data from {}".format(url))
            return None

        if verbose:
            print("Retriving file went well..")

        # Unzip and save file
        self.unzipper.save_zip_content(data.content, directory, verbose=verbose)

    def download_documents(self, document_type, data_format, path):
        """ Download all the documents of a certain format, and type to a path. """
        # Get the correct documents
        for url in self.interface.get_document_uri(data_format, document_type):
            # Download one URL at a time
            self.download_dataset(url, path, verbose=False)

    def download_all_data(self, data_format, path, interface=RiksDatasetInterface(), verbose=True):
        """ Download all the available data, extract and save it to path.
        The data is saved into subfolders corresponding to 'samling' """

        # Make sure format is available
        if data_format not in interface.available_formats():
            print("{} is not a valid format.".format(data_format))
            return None

        # Get all datasets (URLs) with correct formatn
        datasets = interface.available_datasets(data_format)

        if verbose:
            print("Retrived all the datasets with format {}".format(data_format))

        for dataset in datasets:
            # complete URL is needed to get data
            dataset_url = interface.base_url + dataset
            # This is used to save the data into a folder coresponding to samling
            folder = interface.dataset_info(dataset)['samling']

            # Create an individual path for each dataset
            dataset_path = os.path.join(path, folder)

            # Download the dataset
            self.download_dataset(dataset_url, dataset_path, verbose=True)

    #def download_collection()
