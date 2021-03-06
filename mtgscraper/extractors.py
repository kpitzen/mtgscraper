'''handles the extract of data from mtg websites'''
import abc
from urllib.error import HTTPError

import pandas as pd
from numpy import isnan


class MTGExtractor():
    '''abstract class to extend for new mtg websites'''
    __metaclass__ = abc.ABCMeta

    def __init__(self, url):
        self._url = url
        self.__payload = None

    @property
    @abc.abstractproperty
    def deck_data(self):
        '''a pandas dataframe containing decklist returned by url'''
        raise NotImplementedError('NEEDS TO BE OVERRIDDEN')

    @deck_data.setter
    @abc.abstractproperty
    def deck_data(self, url):
        raise NotImplementedError('NEEDS TO BE OVERRIDDEN')


    @property
    @abc.abstractproperty
    def deck_id(self):
        '''numerical id of deck. unique across all decks'''
        raise NotImplementedError('NEEDS TO BE OVERRIDDEN')

    @deck_id.setter
    @abc.abstractproperty
    def deck_id(self, value):
        raise NotImplementedError('NEEDS TO BE OVERRIDDEN')

    @property
    def payload(self):
        '''JSON representation of deck data'''
        return self.__payload

    @payload.getter
    def payload(self):
        return self.deck_data.to_dict(orient='records') #TODO: Add type-formatting for dynamo here?


class MTGGoldFishDeckExtractor(MTGExtractor):
    '''Class intended to access data from MTGGoldfish'''

    def __init__(self, deck_number):
        url = 'https://www.mtggoldfish.com/deck/{}'
        MTGExtractor.__init__(self, url)
        self._deck_data = None
        self.__deck_id = None
        self.deck_data = self._url.format(deck_number)
        print('>>Successfully extracted: {}'.format(self._url.format(deck_number)))
        self.deck_id = deck_number
        self.deck_data['deck_id'] = self.deck_id

    @property
    def deck_data(self):
        '''a pandas dataframe containing decklist returned by url'''
        return self._deck_data

    @deck_data.setter
    def deck_data(self, url):
        try:
            deck_dataframe = pd.read_html(url, attrs={'class': 'deck-view-deck-table'})[0]
            deck_dataframe.columns = ['count', 'name', 'mana_cost', 'price']
            deck_dataframe['row_id'] = deck_dataframe.index
            try:
                filtered_deck_dataframe = deck_dataframe[deck_dataframe['name'].notnull()]
            except KeyError:
                print(deck_dataframe)
                raise
        except HTTPError:
            filtered_deck_dataframe = None
        self._deck_data = filtered_deck_dataframe


    @property
    def deck_id(self):
        '''numerical id of deck. unique across all decks'''
        return self.__deck_id

    @deck_id.setter
    def deck_id(self, value):
        self.__deck_id = int(value)
