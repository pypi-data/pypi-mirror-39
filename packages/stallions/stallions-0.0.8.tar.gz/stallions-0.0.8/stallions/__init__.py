"""
Extract the content of the web page
"""

from .crawler import Crawler
from .version import __version__


class Stallion(object):
    """
    Main class
    """

    def __init__(self, enable_urls=False):
        self.enable_urls = enable_urls

    def extract(self, url, is_file=False, coding=False):
        """
        Main method to extract an article object from a URL,
        pass in a url and get back a Article
        """
        cr = Crawler(is_file, self.enable_urls)
        try:
            article = cr.crawl(url, coding)
        except Exception as e:
            print(e)
            return cr.article
        return article

    def shutdown_network(self):
        pass


s = Stallion()
extract = s.extract
