#!/usr/bin/python3
""" BasicCache module """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ A basic caching system without a limit on the number of items """

    def put(self, key, item):
        """ Add an item to the cache """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is not None:
            return self.cache_data.get(key)
        return None
