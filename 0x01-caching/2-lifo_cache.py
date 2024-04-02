#!/usr/bin/python3
""" LIFOCache module """

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ A caching system using LIFO (Last In, First Out) replacement policy"""

    def __init__(self):
        """ Initialize the LIFO cache """
        super().__init__()

    def put(self, key, item):
        """ Add an item to the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # If cache is full, discard the last item (LIFO)
                discarded_key = list(self.cache_data.keys())[-1]
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is not None:
            return self.cache_data.get(key)
        return None
