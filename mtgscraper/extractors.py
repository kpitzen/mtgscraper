'''handles the extract of data from mtg websites'''
import abc
from urllib.error import HTTPError

import pandas as pd


class MTGExtractor():
    '''abstract class to extend for new mtg websites'''
    __metaclass__ = abc.ABCMeta

    def __init__(self, url):
        self._url = url

class MTGGoldFisDeckhExtractor(MTGExtractor):
    '''Class intended to access data from MTGGoldfish'''

    def __init__(self, deck_number):
        url = 'https://www.mtggoldfish.com/deck/{}'
        MTGExtractor.__init__(self, url)
        self._deck_data = None
        self.__deck_id = None
        self.deck_data = self._url.format(deck_number)
        print('>>Successfully extracted: {}'.format(self._url.format(deck_number)))
        self.deck_id = deck_number

    @property
    def deck_data(self):
        '''a pandas dataframe containing decklist returned by url'''
        return self._deck_data

    @deck_data.setter
    def deck_data(self, url):
        try:
            deck_dataframe = pd.read_html(url, attrs={'class': 'deck-view-deck-table'})[0]
        except HTTPError:
            deck_dataframe = None
        self._deck_data = deck_dataframe


    @property
    def deck_id(self):
        return self.__deck_id

    @deck_id.setter
    def deck_id(self, value):
        self.__deck_id = value