#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieve a page of data with deletion-resilient pagination.

        Args:
            index (int): The start index of the current page
                (None means start from the beginning)
            page_size (int): The number of items per page

        Returns:
            Dict: A dictionary containing pagination
            information and the requested data
        """
        indexed_data = self.indexed_dataset()
        data_length = len(indexed_data)

        if index is None:
            index = 0

        assert 0 <= index < data_length, "Index out of range"

        data = []
        current_index = index
        next_index = min(index + page_size, data_length)

        while len(data) < page_size and current_index < data_length:
            if current_index in indexed_data:
                data.append(indexed_data[current_index])
            current_index += 1

        while current_index < data_length and len(data) < page_size:
            if current_index in indexed_data:
                data.append(indexed_data[current_index])
            current_index += 1

        return {
            "index": index,
            "next_index": current_index,
            "page_size": len(data),
            "data": data
        }
