#!/usr/bin/python3
""" LFUCache module """
from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """A caching system using LFU (Least Frequently Used)replacement policy"""

    def __init__(self):
        """ Initialize the LFU cache """
        super().__init__()
        self.frequency = defaultdict(int)

    def put(self, key, item):
        """ Add an item to the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # If cache is full, discard the least frequency used item(LFU)
                minf = min(self.frequency.values())
                lfu_keys = [k for k, v in self.frequency.items() if v == minf]
                if len(lfu_keys) > 1:
                    # If more than one LFU item, use LRU to break tie
                    lru_key = min(self.cache_data, key=self.frequency.get)
                    del self.cache_data[lru_key]
                    del self.frequency[lru_key]
                    print(f"DISCARD: {lru_key}")
                else:
                    lfu_key = lfu_keys[0]
                    del self.cache_data[lfu_key]
                    del self.frequency[lfu_key]
                    print(f"DISCARD: {lfu_key}")
            self.cache_data[key] = item
            self.frequency[key] += 1

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is not None:
            if key in self.cache_data:
                self.frequency[key] += 1
                return self.cache_data[key]
        return None