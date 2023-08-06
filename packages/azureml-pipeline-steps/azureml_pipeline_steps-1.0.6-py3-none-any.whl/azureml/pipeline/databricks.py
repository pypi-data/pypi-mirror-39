# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""databricks.py.

Module for creating AutoScale for a Databricks step.
"""


class AutoScale:
    """
    Creates an AutoScale input for a Databricks step.

    :param min_workers: The min number of workers for the databricks run cluster.
    :type min_workers: int
    :param max_workers: The max number of workers for the databricks run cluster.
    :type max_workers: int
    """

    def __init__(self, min_workers=None, max_workers=None):
        """
        Initialize AutoScale.

        :param min_workers: The min number of workers for the databricks run cluster.
        :type min_workers: int
        :param max_workers: The max number of workers for the databricks run cluster.
        :type max_workers: int
        """
        if min_workers is None:
            raise ValueError("min_workers is required")
        if not isinstance(min_workers, int):
            raise ValueError("min_workers must be an int")
        if max_workers is None:
            raise ValueError("max_workers is required")
        if not isinstance(max_workers, int):
            raise ValueError("max_workers must be an int")

        self.min_workers = min_workers
        self.max_workers = max_workers
