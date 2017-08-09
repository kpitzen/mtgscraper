'''Handles process flow for mtg data'''

import argparse
import random
import pickle
import boto3
from os.path import join
from multiprocessing import Pool

from mtgscraper import extractors, loaders

DATA_DIR = 'data'

ARG_PARSER = argparse.ArgumentParser()
ARG_PARSER.add_argument('-a', '--all', help='Sets all boolean switches to true for given process'
                        , action='store_true')
SUBPARSERS = ARG_PARSER.add_subparsers(dest='subparser_name')
EXTRACT_PARSER = SUBPARSERS.add_parser('extract')
EXTRACT_PARSER.add_argument('-gf', '--goldfish', action='store_true'
                            , help='Extract MTGGoldfish Data')
LOAD_PARSER = SUBPARSERS.add_parser('load')
LOAD_PARSER.add_argument('-d', '--decks', action='store_true'
                         , help='Load deck data to dynamodb')
ARGS = ARG_PARSER.parse_args()

if __name__ == '__main__':

    EXTRACTORS = None

    if ARGS.subparser_name == 'extract':
        if ARGS.goldfish:
            EXTRACT_POOL = Pool(5)
            EXTRACTORS = EXTRACT_POOL.map(extractors.MTGGoldFishDeckExtractor
                                          , random.choices(range(1, 100000, 1), k=20))
            for extractor in EXTRACTORS:
                print(extractor.deck_data, extractor.deck_id)
        with open(join(DATA_DIR, 'goldfish_extract.bin'), 'wb') as extract_file:
            pickle.dump(EXTRACTORS, extract_file)

    if ARGS.subparser_name == 'load':
        LOAD_DATA = []
        if ARGS.decks:
            CLIENT_SESSION = boto3.client('dynamodb')
            DATA_LOADER = loaders.MTGDeckLoader(CLIENT_SESSION)
            with open(join(DATA_DIR, 'goldfish_extract.bin'), 'rb') as extract_file:
                LOAD_DATA = pickle.load(extract_file)
            for data_element in LOAD_DATA:
                try:
                    DATA_LOADER.load_data(data_element)
                except Exception:
                    raise
                else:
                    print('>>Successfully loaded: {}'.format(data_element.deck_id))
