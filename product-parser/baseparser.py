from queuefetcher.threadurl import ThreadUrl

__author__ = 'cliu'


class BaseParser(ThreadUrl):
    def __init__(self):
        ThreadUrl.__init__(self)