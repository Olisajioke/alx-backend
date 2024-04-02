#!/usr/bin/python3
""" MRUCache module """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ A caching system using MRU (Most Recently Used) replacement policy """

    def __init__(self):
        """ Initialize the MRU cache """
        super().__init__()
        self.access_order = []

    def put(self, key, item):
        """ Add an item to the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # If cache is full, discard the most recently used item (MRU)
                mru_key = self.access_order.pop()
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")
            self.cache_data[key] = item
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)

    def get(self, key):
        """ Retrieves an item from the cache """
        if key is not None:
            if key in self.cache_data:
                self.access_order.remove(key)
                self.access_order.append(key)
                return self.cache_data[key]
        return None
