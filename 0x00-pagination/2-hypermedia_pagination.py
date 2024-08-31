#!/usr/bin/env pyton3
""" Hypermedia pagination"""
import csv
import math
from typing import List, Tuple, Dict, Union


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end indexes for pagination.

    Args:
    page (int): The current page number (1-indexed)
    page_size (int): The number of items per page

    Returns:
    tuple: A tuple containing the start and end indexes
    """
    if page < 1 or page_size < 1:
        return (0, 0)

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return (start_index, end_index)


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a specific page of data from the dataset.

        Args:
        page (int): The page number to retrieve (1-indexed)
        page_size (int): The number of items per page

        Returns:
        List[List]: A list of rows for the specified page
        """
        assert isinstance(
                page, int) and page > 0, "page must be a positive integer"
        assert isinstance(
                page_size, int
                ) and page_size > 0, "page_size must be a positive integer"

        dataset = self.dataset()
        start, end = index_range(page, page_size)

        if start >= len(dataset):
            return []

        return dataset[start:end]

    def get_hyper(
            self, page: int = 1, page_size: int = 10
            ) -> Dict[str, Union[int, List[List], None]]:
        """
        Retrieve a page of data along with pagination information.

        Args:
        page (int): The page number to retrieve (1-indexed)
        page_size (int): The number of items per page

        Returns:
            Dict: A dictionary containing pagination information
            and the requested data
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
            }
