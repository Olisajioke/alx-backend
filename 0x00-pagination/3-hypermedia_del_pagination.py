#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Union


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Return hypermedia pagination data based on index."""
        dataset = self.indexed_dataset()
        total_items = len(dataset)
        max_index = total_items - 1
        max_page = math.ceil(total_items / page_size)
        max_index_for_last_page = (max_page - 1) * page_size

        # Validate index
        assert1 = "Index must be an integer"
        assert index is None or isinstance(index, int), assert1
        if index is not None:
            assert 0 <= index <= max_index, "Index out of range"

        # Calculate start and end index for the current page
        start_index = index if index is not None else 0
        end_index = min(start_index + page_size, total_items)

        # Calculate next index
        next_index = end_index if end_index < max_index else None

        return {
            'index': start_index,
            'next_index': next_index,
            'page_size': page_size,
            'data': [dataset[i] for i in range(start_index, end_index)]
        }
