'''Handles process flow for mtg data'''

import argparse
import random
import pickle
from os.path import join
from multiprocessing import Pool

from mtgscraper import extractors

DATA_DIR = 'data'

ARG_PARSER = argparse.ArgumentParser()
ARG_PARSER.add_argument('-a', '--all', help='Sets all boolean switches to true for given process'
                        , action='store_true')
SUBPARSERS = ARG_PARSER.add_subparsers(dest='subparser_name')
EXTRACT_PARSER = SUBPARSERS.add_parser('extract')
EXTRACT_PARSER.add_argument('-gf', '--goldfish', action='store_true'
                            , help='Extract MTGGoldfish Data')
ARGS = ARG_PARSER.parse_args()

if __name__ == '__main__':

    if ARGS.subparser_name == 'extract':
        if ARGS.goldfish:
            EXTRACT_POOL = Pool(5)
            EXTRACTORS = EXTRACT_POOL.map(extractors.MTGGoldFisDeckhExtractor
                                          , random.choices(range(1, 100000, 1), k=20))
        with open(join(DATA_DIR, 'goldfish_extract.bin'), 'wb') as extract_file:
            pickle.dump(EXTRACTORS, extract_file)
