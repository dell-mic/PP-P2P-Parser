#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright 2018-03-17 ChrisRBe
import argparse
import logging
import os
import sys

from src import mintos_parser, portfolio_performance_writer


def platform_factory(operator_name='mintos'):
    """
    Return an object for the required Peer-to-Peer lending platform

    :param operator_name: name of the P2P lending site, defaults to Mintos
    :return: object for the actual lending platform parser, None if not supported
    """
    if operator_name == 'mintos':
        return mintos_parser.MintosParser()
    else:
        logging.error('The provided platform {} is currently not supported'.format(operator_name))
        return False


def main(infile, p2p_operator_name='mintos'):
    """
    Processes the provided input file with the rules defined for the given platform.
    Outputs a CSV file readable by Portfolio Performance

    :param infile: input file containing the account statements from a supported platform
    :param p2p_operator_name: name of the Peer-to-Peer lending platform, defaults to Mintos
    :return: True, False if an error occurred.
    """
    if not os.path.exists(infile):
        logging.error('provided file {} does not exist'.format(infile))
        return False

    platform_parser = platform_factory(p2p_operator_name)
    if platform_parser:
        platform_parser.account_statement_file = infile
        statement_list = platform_parser.parse_account_statement()

        writer = portfolio_performance_writer.PortfolioPerformanceWriter()
        writer.init_output()
        for entry in statement_list:
            writer.update_output(entry)
        writer.write_pp_csv_file(os.path.join(os.path.dirname(infile),
                                              'portfolio_performance__{}.csv'.format(p2p_operator_name)))
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=str,
                        help='CSV file containing the downloaded data from the P2P site')
    parser.add_argument('--type',
                        type=str,
                        help='Specifies the format of the input file (different for each P2P service)')
    parser.add_argument('--debug',
                        action='store_true',
                        help='enables debug level logging if set')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    sys.exit(main(args.infile, args.type))