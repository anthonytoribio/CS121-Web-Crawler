from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
import os


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    if restart:
        #delete wordFreq.json & subDomains.json & url.txt
        if os.path.isfile(os.path.dirname(__file__) + "subDomains.json"):
            os.remove(os.path.dirname(__file__) + "subDomains.json")
        if os.path.isfile(os.path.dirname(__file__) + "wordFreq.json"):
            os.remove(os.path.dirname(__file__) + ".json")
        open("/Logs/urls.txt", "w").close()
        open("/Logs/page_length.txt", "w").close()

    crawler.start()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
