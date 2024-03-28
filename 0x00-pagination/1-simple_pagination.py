#!/usr/bin/env python
"""A simple pagination helper function."""

import csv
from typing import List, Tuple
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return the start and end index for a given page and page size."""
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """A simple server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset METHOD.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the appropriate page of the dataset."""
        assert1 = "Page must be a positive integer"
        assert2 = "Page size must be a positive integer"
        assert isinstance(page, int) and page > 0, assert1
        assert isinstance(page_size, int) and page_size > 0, assert2

        dataset = self.dataset()
        total_pages = math.ceil(len(dataset) / page_size)
        if page > total_pages:
            return []

        start_index, end_index = index_range(page, page_size)
        return dataset[start_index:end_index]
