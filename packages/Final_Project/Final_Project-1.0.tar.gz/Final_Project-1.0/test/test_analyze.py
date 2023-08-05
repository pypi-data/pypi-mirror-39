#!usr/bin/python
"""Unittest for Analyze.py.
"""
import unittest
import os
import pandas as pd
from webcrawler.analyze import graph_scatter, graph_boxplot

__author__ = "Disaiah Bennett"
__version__ = "1.0"

class TestAnalyze(unittest.TestCase):
    """Unittest for Analyze
    """
#    def __init__(self, file_name=None, columns=None, records=None, frame=None):
#        self.file_name = file_name
#        self.columns = columns
#        self.records = records
#        self.frame = frame

    def test_graph_scatter_001(self):
        """Testing graph_scatter.
        """
        file_name = os.listdir(".")
        columns = ["Address", "Year", "Size", "Price"]
        records = []
        frame = pd.DataFrame()
        try:
            for files in file_name:
                if ".csv" in files:
                    records.append(pd.read_csv(files, header=None, names=columns))
                    frame = pd.concat(records)
            if records:
                try:
                    graph_scatter(frame)
                except ValueError:
                    pass
        except OSError:
            pass

    def test_graph_boxplot_002(self):
        """Testing graph_boxplot.
        """
        file_name = os.listdir(".")
        columns = ["Address", "Year", "Size", "Price"]
        records = []
        frame = pd.DataFrame()
        try:
            for files in file_name:
                if ".csv" in files:
                    records.append(pd.read_csv(files, header=None, names=columns))
                    frame = pd.concat(records)
            if records:
                try:
                    graph_boxplot(frame)
                except ValueError:
                    pass
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
