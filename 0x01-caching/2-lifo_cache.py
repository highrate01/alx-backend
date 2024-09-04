#!/usr/bin/env python3
"""LIFO IMPLEMENTAION"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """class LIFOCache that inherits from BaseCaching
    and is a caching system"""
    def __init__(self):
        """initializes"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """assign to the dictionary self.cache_data the
        item value for the key key"""
        if key is None or item is None:
            return
        if len(self.cache_data) >= self.MAX_ITEMS \
                and key not in self.cache_data:
            discarded_data = self.order.pop()
            del self.cache_data[discarded_data]
            print(f"DISCARD: {discarded_data}")

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data:
            return
        return self.cache_data[key]
