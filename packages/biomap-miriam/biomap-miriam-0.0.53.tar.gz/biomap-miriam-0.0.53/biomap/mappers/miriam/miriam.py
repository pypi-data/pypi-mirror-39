import os
import json

import requests
from lxml import etree

from biomap.utils import local_path
from biomap.utils.xml import xml_to_json
from biomap.core.insert import MapInserter

MIRIAM_DEFAULT_DOWNLOAD_URL='https://www.ebi.ac.uk/miriam/main/export/xml'
__LOCAL_PATH__ = local_path('download/miriam')

class MIRIAM:
    def __init__(self, download_url=MIRIAM_DEFAULT_DOWNLOAD_URL,
                       local_path=__LOCAL_PATH__):
        self.download_url = download_url
        self.local_path = local_path
        self.local_file = os.path.join(local_path, 'miriam_registry.xml')

    def download(self):
        response = requests.get(self.download_url)
        if response.status_code != 200:
            print("ERROR")
            return False
        with open(self.local_file, 'wb') as fp:
            fp.write( response.content )
        return True

    def get(self, how='json'):
        if not os.path.isfile(self.local_file):
            success = self.download()
            if not success:
                return None
        if how == 'bytes':
            with open(self.local_file, 'rb') as fp:
                return fp.read()
        elif how == 'xml':
            return etree.XML(self.get(how='bytes'))
        elif how == 'json':
            return xml_to_json(self.get(how='xml'), '}')
        return None

class MiriamInserter(MapInserter):
    def __init__(self, **kwargs):
        self.miriam = MIRIAM(**kwargs)
        self.data = self.miriam.get()

    def mapper_data(self):
        docs = self.data['datatype']
        for doc in docs:
            doc['uri'] = [uri['uri'] for uri in doc['uris']]
        return docs

    def mapper_definition(self):
        '''
        docs must be here.
        '''
        supported_keys = {key for doc in self.data['datatype'] for key in doc.keys()}
        key_synonyms = { 'miriam_'+key : key for key in supported_keys }
        list_valued_keys = ['uris', 'synonyms']
        disjoint = ['uris']
        compound_valued_keys = ['resources', 'annotation', 'documentations', 'uris']
        return {
                 'name': 'miriam',
                 'mapper_data' : 'miriam',
                 'supported_keys': list(supported_keys),
                 'main_key' : 'namespace',
                 'key_synonyms' : key_synonyms,
                 'list_valued_keys': list_valued_keys,
                 'disjoint': disjoint,
                 'compound_valued_keys': compound_valued_keys
               }

inserters = [
    MiriamInserter
]
