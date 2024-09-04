#!/usr/bin/env python3
"""FIFO caching"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """A FIFO caching system"""
    def __init__(self):
        """initializes"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """assign to the dictionary self.cache_data the
        item value for the key"""
        if key is None or item is None:
            return
        if len(self.cache_data) >= self.MAX_ITEMS \
                and key not in self.cache_data:
            discarded_key = self.order.pop(0)
            del self.cache_data[discarded_key]
            print(f"DISCARD: {discarded_key}")
        self.cache_data[key] = item
        if key not in self.order:
            self.order.append(key)

    def get(self, key):
        """return the value in self.cache_data linked to key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
