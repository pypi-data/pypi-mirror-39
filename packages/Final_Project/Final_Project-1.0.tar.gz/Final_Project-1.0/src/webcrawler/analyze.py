#!/usr/bin/python
"""Analyze Module, was designed to analyze and plot csv data into a scatter and box plot graph.
"""
import os
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.switch_backend('agg')
warnings.filterwarnings("ignore", category=RuntimeWarning)

def graph_scatter(frame):
    """CSV data scatter plot. Plots are made from the house price and size.
    """
    print frame
    _, graph = plt.subplots()
    graph.set_xlabel('Size: sqft/acres', size=12)
    graph.set_ylabel('Prices', size=12)
    graph.set_title("House's Size and Price")

    color = np.random.random(len(frame))

    graph.scatter(x=frame["Size"], y=frame["Price"], c=color)
    plt.savefig("../other/size_price.png")

    #img = Image.open("size_price.png")
    #img.show()

def graph_boxplot(frame):
    """CSV data box plot. Plots are made from the house ratios (price/size) and grouped by year.
    """
    frame["Ratio"] = frame["Price"] / frame["Size"]
    print frame

    try:
        graph = frame.boxplot(column="Ratio", by="Year")
        graph.set_xticklabels(frame['Year'], rotation=90)
        graph.set_ylim(-10, 175)
    except RuntimeError:
        pass

    plt.savefig("../other/ratio.png")

    #img = Image.open("../ratio.png")
    #img.show()

def main():
    """Analyze and create a scatter and box plot.
    """
    rec_columns = ['Address', 'Year', 'Size', 'Price'] # Records Columns.

    files_name = os.listdir("./csv")
    frame = pd.DataFrame() # Create dataframe.
    records = [] # Empty list for dataset records.

    try:
        os.chdir("./csv")
    except OSError:
        pass

    for files in files_name:
        if ".csv" in files:
            records.append(pd.read_csv(files, header=None, names=rec_columns))

    frame = pd.concat(records)

    graph_scatter(frame)
    plt.close()
    graph_boxplot(frame)

if __name__ == "__main__":
    main()
