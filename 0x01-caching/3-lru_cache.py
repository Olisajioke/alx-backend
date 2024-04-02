#!/usr/bin/python3
""" LRUCache module """

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ A caching system using LRU (Least Recently Used) replacement policy"""

    def __init__(self):
        """ Initialize the LRU cache """
        super().__init__()
        self.access_order = []

    def put(self, key, item):
        """ Add an item to the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                if self.access_order:
                    # If cache is full and access_order is
                    # not empty, discard the least recently used item (LRU)
                    lru_key = self.access_order.pop(0)
                    del self.cache_data[lru_key]
                    print(f"DISCARD: {lru_key}")
            else:
                self.access_order.append(key)
            self.cache_data[key] = item
        elif key in self.cache_data:
            self.access_order.remove(key)

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is not None:
            if key in self.cache_data:
                if key in self.access_order:
                    self.access_order.remove(key)
                self.access_order.append(key)
                return self.cache_data[key]
        return None
