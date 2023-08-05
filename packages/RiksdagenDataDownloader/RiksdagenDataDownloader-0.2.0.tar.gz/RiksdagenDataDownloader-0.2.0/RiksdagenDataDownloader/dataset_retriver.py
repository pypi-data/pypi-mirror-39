import requests
import xmltodict


class RiksDatasetInterface:
    """ A class which acts as an interface to get URIs for the
    available datasets. It does this by downloading and parse
    an XML provided by riksdagen. The class will automatically
    be initilized with a link to an URL.
    Dataset URL last checked: 2018-12-02
    If it doesn't work you can initilize the class with another
    URI.
    """

    def __init__(self, xml_url='http://data.riksdagen.se/dataset/katalog/dataset.xml'):
        self.data_formats = []
        self.data_types = []
        self.collections = []

        # Base url to riksdagen data
        self.base_url = 'http://data.riksdagen.se'
        # Holds datasets according to format
        self.format_dataset = dict()
        # A dictionary which holds info about an URL
        self.url_info = dict()

        # Get the metadata and return xmltodict object
        xml_dict = self._get_meta_data(xml_url)

        # If unsucesful
        if xml_dict is None:
            print("Something went wrong when retriving the dataset, make \
            sure the URL is correct.")
        else:
            # Parse data int above dictionaries
            self._parse_data(xml_dict)

    def _get_meta_data(self, xml_url):
        """ Helper method to retrive the XML with meta data """
        # Get the XML file
        data_xml = requests.get(xml_url)

        # Make sure we sure we got an OK
        if data_xml.status_code == 200:
            clean_xml = ''
            # Change bytes to UTF-8 string
            for line in data_xml.iter_lines():
                clean_xml += line.decode('utf-8')

            xml_dict = xmltodict.parse(clean_xml)
            return xml_dict
        return None

    def _parse_data(self, xml_dict):
        """ Helper method to parse the data into new dictionaries"""
        try:
            for dataset in xml_dict['datasetlista']['dataset']:
                if dataset.get('typ', None) not in self.data_types:
                    self.data_types.append(dataset['typ'])

                if dataset.get('samling', None) not in self.collections:
                    self.collections.append(dataset['samling'])

                # Format to URLs
                self.format_dataset[dataset['format']] = \
                self.format_dataset.get(dataset['format'], []) + [dataset['url']]
                # URL represents a dataset, which hold info
                self.url_info[dataset['url']] = dataset

            self.data_formats = list(self.format_dataset.keys())
        except:
            print("Something went wrong when parsing the XML file")

    def available_datasets(self, data_format='json'):
        """ Yields the list for all available datasets """
        for dataset in self.format_dataset.get(data_format, []):
            yield dataset

    def datasets_with_format(self, data_format=None):
        """ Returns a list of all the available datasets for
        a given data formats """

        # If no specific format given, return all of them
        if not data_format:
            dSets = []
            for dSet in self.format_dataset.keys():
                dSets.extend(self.format_dataset[dSet])
            return dSets
        # Otherwise return the sets for format or empty list
        else:
            return self.format_dataset.get(data_format, [])

    def available_doc_types(self):
        """ Returns a list of all the available document types"""
        doc_types = []
        for dataset in self.available_datasets():
            if self.dataset_info(dataset)['namn'] not in doc_types:
                doc_types.append(self.dataset_info(dataset)['namn'])
        return doc_types

    def dataset_info(self, url):
        """ Returns a dictionary with all the info for dataset """
        return self.url_info.get(url, None)

    def get_all_dataset_uri(self, data_format='json'):
        """ Yield all the URIs to all the available datasets of that type. """
        for dataset in self.available_datasets(data_format):
            yield dataset

    def get_all_dataset_uri_size(self, data_format='json'):
        """ Yield all the URIs to all the available datasets of that type
        and the size of the dataset as a tuple. """
        for dataset in self.available_datasets(data_format):
            yield (self.base_url + dataset, self.dataset_info(dataset)['storlek'])

    def get_document_uri(self, data_format='json', doc_type=''):
        """ Yield all the URIs for given document type. """
        for dataset in self.available_datasets(data_format):
            if doc_type == '' or self.dataset_info(dataset)['namn'] == doc_type:
                yield dataset

    # These methods are repetative.
    # It is meant this way to make the interface easier.
    def get_all_anforande_uri(self, data_format='json'):
        """ Yield all the URIs for document type anforande. """
        for dataset in self.get_document_uri(data_format, 'anforande'):
            yield self.base_url + dataset

    def get_all_dokument_uri(self, data_format='json'):
        """ Yield all the URIs for document type dokument. """
        for dataset in self.get_document_uri(data_format, 'dokument'):
            yield self.base_url + dataset

    def get_all_person_uri(self, data_format='json'):
        """ Yield all the URIs for document type person. """
        for dataset in self.get_document_uri(data_format, 'person'):
            yield self.base_url + dataset

    def get_all_votering_uri(self, data_format='json'):
        """ Yield all the URIs for document type votering. """
        for dataset in self.get_document_uri(data_format, 'votering'):
            yield self.base_url + dataset
