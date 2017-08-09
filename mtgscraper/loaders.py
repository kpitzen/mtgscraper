'''handles loading of data to dynamodb via boto3'''

import abc
import datetime

class MTGLoader():
    '''abstract loader class'''

    __metaclass__ = abc.ABCMeta

    def __init__(self, session):
        self._session = session
        self._primary_key = None

    @property
    @abc.abstractproperty
    def primary_key(self):
        raise NotImplementedError('This needs to be overridden!')

    @primary_key.getter
    @abc.abstractproperty
    def primary_key(self):
        raise NotImplementedError('This needs to be overridden!')
    
    @abc.abstractmethod
    def load_data(self, input_data):
        raise NotImplementedError('This needs to be overridden!')

class MTGDeckLoader(MTGLoader):
    '''handles loading of mtg deck information'''

    def __init__(self, session):
        MTGLoader.__init__(self, session)

    @property
    def primary_key(self):
        return self._primary_key

    @primary_key.getter
    def primary_key(self):
        return datetime.datetime.now()

    def load_data(self, input_data):
        input_payload = input_data.payload
        print(input_payload)
        for row in input_payload:
            print(row) #TODO: Or maybe we add that type inference here?
            row['creation_time'] = str(self.primary_key)
            self._session.put_item(TableName='mtgdecks',
                                   Item=row)
