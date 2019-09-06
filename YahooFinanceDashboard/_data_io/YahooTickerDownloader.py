
# Adapted from: https://github.com/Benny-/Yahoo-ticker-symbol-downloader/blob/master/YahooTickerDownloader.py

"""
Copyright (c) 2016, Benny Jacobs
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Benny Jacobs BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import pickle
from time import sleep
import argparse
import io
import logging

import tablib
import sqlite3

from ytd import SimpleSymbolDownloader
from ytd.downloader.GenericDownloader import GenericDownloader
from ytd.compat import text
from ytd.compat import csv
from ytd.compat import robotparser


logger = logging.getLogger(__name__)


user_agent = SimpleSymbolDownloader.user_agent

options = {"generic": GenericDownloader()}

formats = ['csv', 'xlsx', 'json', 'yaml', 'sqlite']


def loadDownloader(tickerType):
    """loads from intermediate pickle file
    """
    with open(tickerType + ".pickle", "rb") as f:
        return pickle.load(f)


def saveDownloader(downloader, tickerType):
    """saves to intermediate pickle file
    """
    with open(tickerType + ".pickle", "wb") as f:
        pickle.dump(downloader, file=f, protocol=pickle.HIGHEST_PROTOCOL)


def downloadEverything(downloader, tickerType, insecure, sleeptime, pandantic):

    loop = 0
    while not downloader.isDone():

        symbols = downloader.nextRequest(insecure, pandantic)
        logger.info(f"Got {str(len(symbols))} downloaded {downloader.type} symbols:")
        if(len(symbols) > 2):
            try:
                logger.info(f" {text(symbols[0])}")
                logger.info(f" {text(symbols[1])}")
                logger.info("  ect...")
            except:
                logger.warning(" Could not display some ticker symbols due to char encoding")
        downloader.printProgress()

        # Save download state occasionally.
        # We do this in case this long running is suddenly interrupted.
        loop = loop + 1
        if loop % 200 == 0:
            logger.info("Saving downloader to disk...")
            saveDownloader(downloader, tickerType)
            logger.info("Downloader successfully saved.")

        if not downloader.isDone():
            sleep(sleeptime)  # So we don't overload the server.


def exportFile(data, downloader, file_format):

    exporting_function = {'xlsx': data.xlsx,
                          'json': data.json.encode('UTF-8'),
                          'yaml': data.yaml.encode('UTF-8')}

    if file_format == 'csv':
        with io.open(downloader.type + '.csv', 'w', encoding='utf-8') as f:
            f.write(text.join(u',', data.headers) + '\n')
            writer = csv.writer(f)
            for i in range(0, len(data)):
                row = [text(y) if not y is None else u"" for y in data[i]]
                writer.writerow(row)

    elif file_format == 'sqlite':
        db = sqlite3.connect(f'{downloader.type}.{file_format}')
        df = data.export('df')
        df.to_sql('YAHOO_TICKERS', db, if_exists='replace')
        db.commit()
        db.close()

    elif file_format in [item for item in formats if item != 'csv']:
        try:
            with open(f'{downloader.type}.{file_format}', 'wb') as f:
                f.write(exporting_function[file_format])
        except:
            logger.warning(f"Could not export .{file_format} due to a internal error")
    else:
        logger.error('Unknown output format')

def main():
    downloader = None

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help=f"Output format to store tickers data. Options are: {' '.join(formats)}", default='sqlite')
    parser.add_argument("-i", "--insecure", help="use HTTP instead of HTTPS", action="store_true")
    parser.add_argument("-e", "--export", help="export immediately without downloading (Only useful if you already downloaded something to the .pickle file)", action="store_true")
    parser.add_argument('-E', '--Exchange', help='Only export ticker symbols from this exchange (the filtering is done during the export phase)')
    parser.add_argument('type', nargs='?', default='generic', help='The type to download, this can be: '+" ".join(list(options.keys())))
    parser.add_argument("-s", "--sleep", help="The time to sleep in seconds between requests", type=float, default=0)
    parser.add_argument("-p", "--pandantic", help="Stop and warn the user if some rare assertion fails", action="store_true")

    args = parser.parse_args()

    protocol = 'http' if args.insecure else 'https'
    if args.insecure:
        logger.info("Using insecure connection")

    if args.export:
        logger.info("Exporting pickle file")

    tickerType = args.type = args.type.lower()

    logger.info("Checking if we can resume a old download session")
    try:
        downloader = loadDownloader(tickerType)
        logger.info("Downloader found on disk, resuming")
    except:
        logger.info("No old downloader found on disk. Starting a new session")
        if tickerType not in options:
            logger.error(f"Error: {tickerType} is not a valid type option. See --help")
            exit(1)
        else:
            downloader = options[tickerType]

    rp = robotparser.RobotFileParser()
    rp.set_url(protocol + '://finance.yahoo.com/robots.txt')
    rp.read()
    try:
        if not args.export:
            
            if(not rp.can_fetch(user_agent, protocol + '://finance.yahoo.com/_finance_doubledown/api/resource/searchassist')):
                logger.warning('Execution of script halted due to robots.txt')
                return 1
            
            if not downloader.isDone():
                logger.info(f"Downloading {downloader.type}")
                downloadEverything(downloader, tickerType, args.insecure, args.sleep, args.pandantic)
                logger.info("Saving downloader to disk...")
                saveDownloader(downloader, tickerType)
                logger.info("Downloader successfully saved.")
            else:
                logger.info("The downloader has already finished downloading everything")

    except Exception as ex:
        logger.error("A exception occurred while downloading. Suspending downloader to disk")
        saveDownloader(downloader, tickerType)
        logger.error("Successfully saved download state")
        logger.error("Try removing {type}.pickle file if this error persists")
        logger.error("Issues can be reported on https://github.com/Benny-/Yahoo-ticker-symbol-downloader/issues")
        raise
    except KeyboardInterrupt as ex:
        logger.warning("Suspending downloader to disk as pickle file")
        saveDownloader(downloader, tickerType)

    if downloader.isDone() or args.export:
        logger.info(f"Exporting {downloader.type} symbols")

        data = tablib.Dataset()
        data.headers = downloader.getRowHeader()

        for symbol in downloader.getCollectedSymbols():
            if(args.Exchange == None):
                data.append(symbol.getRow())
            elif (symbol.exchange == args.Exchange):
                data.append(symbol.getRow())

        exportFile(data, downloader, args.output)

        return data

if __name__ == "__main__":
    data = main()
