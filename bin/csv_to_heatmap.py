import numpy as np
from numpy import vstack  # VSTACK((a,b)) stacks B on TOP of A
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import math
import argparse
import sys


def csv_to_numpy(csv_file):
    """
    Reads in a CSV file and returns a numpy array
    :param csv_file: String, the location and name of the CSV file
    :return: a Numpy array the dimensions of the CSV
    """
    with open(csv_file, 'r') as infile:
        lines = infile.readlines()
    stack = None
    for line in lines:
        newline = []
        for x in [int(y) for y in line.split(',')]:
            if x <= 0:
                newline.append(0)
            else:
                newline.append(math.log(x, 10))
        x = np.array(newline)
        if not stack:
            stack = x
        else:
            try:
                stack = vstack((stack, x))  # Double (( )) on purpose
            except Exception as e:
                if False:
                    print('Error: cannot vstack len:{}'.format(len(x)))
    return stack


def sort_numpy_array(numpy_array):
    """
    Sorts a 2d Numpy array by the sum of each row (highest sum is at the top)
    :param numpy_array: A 2d numpy array
    :return: a sorted 2d numpy array
    """
    numpy_array = numpy_array.tolist()
    numpy_array.sort(key=sum, reverse=True)
    numpy_array = np.array(numpy_array)
    return numpy_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads in a CSV file and outputs a basic heatmap of the data')
    parser.add_argument('-i', '--input', help='The location of the CSV file to be made into a heatmap', required=True)
    parser.add_argument('-o', '--output', help='File name of the figure', required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    csv_array = csv_to_numpy(args.input)
    csv_array = sort_numpy_array(csv_array)

    # This is where you can customize your figure! --------
    # Documentation for the seaborn heatmap can be found here:
    # http://seaborn.pydata.org/generated/seaborn.heatmap.html
    # Feel free to change this to suit your needs, csv_array is a 2d numpy array
    #  of the data to be plotted, and most graphing modules can read numpy arrays
    ax = sns.heatmap(csv_array, xticklabels=[], yticklabels=[])




    # plt.show()  # Uncommenting this line will show the figure before saving
    plt.savefig(args.output)






