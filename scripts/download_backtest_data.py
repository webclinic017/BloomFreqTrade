#!/usr/bin/env python3

"""This script generate json data from bittrex"""
import json
import logging
import os
import sys
from argparse import Namespace
from typing import List

import arrow

from freqtrade import exchange, arguments, misc
from freqtrade.configuration import Configuration

DEFAULT_DL_PATH = 'user_data/data'

logger = logging.getLogger('freqtrade')


def download_parse_args(args: List[str]) -> Namespace:
    """
    Parse args passed to the script
    :param args: Cli arguments
    :return: args: Array with all arguments
    """

    _args = arguments.Arguments(args, 'Download utility')
    _args.testdata_dl_options()
    _args.common_args_parser()
    return _args.parse_args()


def download_backtesting_data(args: Namespace) -> None:
    timeframes = args.timeframes

    dl_path = os.path.join(DEFAULT_DL_PATH, args.exchange)
    if args.export:
        dl_path = args.export

    if not os.path.isdir(dl_path):
        sys.exit(f'Directory {dl_path} does not exist.')

    pairs_file = args.pairs_file if args.pairs_file else os.path.join(dl_path, 'pairs.json')
    if not os.path.isfile(pairs_file):
        sys.exit(f'No pairs file found with path {pairs_file}.')

    with open(pairs_file) as file:
        pairs = list(set(json.load(file)))

    since_time = None
    if args.days:
        since_time = arrow.utcnow().shift(days=-args.days).timestamp * 1000

    logger.info(f'About to download pairs: {pairs} to {dl_path}')

    # Init exchange
    exchange._API = exchange.init_ccxt({'key': '',
                                        'secret': '',
                                        'name': args.exchange})

    for pair in pairs:
        for tick_interval in timeframes:
            logging.info(f'Downloading pair {pair}, interval {tick_interval} ...')

            data = exchange.get_ticker_history(pair, tick_interval, since_ms=since_time)
            if not data:
                logging.warning(' No data was downloaded')
                break

            logging.info(' Data was downloaded for period %s - %s' % (
                arrow.get(data[0][0] / 1000).format(),
                arrow.get(data[-1][0] / 1000).format()))

            # save data
            pair_print = pair.replace('/', '_')
            filename = f'{pair_print}-{tick_interval}.json'
            misc.file_dump_json(os.path.join(dl_path, filename), data)


def main(sysargv: List[str]) -> None:
    """
    This function will initiate the bot and start the trading loop.
    :return: None
    """
    logger.info('Starting Plot Dataframe')
    args = download_parse_args(sysargv)
    Configuration(args).load_config()
    download_backtesting_data(args)


if __name__ == '__main__':
    main(sys.argv[1:])
