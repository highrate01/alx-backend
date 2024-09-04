#!/usr/bin/env python3
"""LRU Caching"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """inherits from BaseCaching and is a caching system"""
    def __init__(self):
        """initializer"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """assign to the dictionary self.cache_data
            the item value for the key key"""
        if key is None or item is None:
            return None
        if len(self.cache_data) >= self.MAX_ITEMS and \
                key not in self.cache_data:
            discarded_data = self.order.pop(0)
            del self.cache_data[discarded_data]
            print(f"DISCARD: {discarded_data}")

        self.cache_data[key] = item
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
